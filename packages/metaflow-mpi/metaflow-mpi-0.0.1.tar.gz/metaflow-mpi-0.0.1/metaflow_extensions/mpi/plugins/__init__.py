import metaflow
from metaflow.unbounded_foreach import UBF_CONTROL
from metaflow.plugins.parallel_decorator import ParallelDecorator, _local_multinode_control_task_step_func
from metaflow.exception import MetaflowException
import subprocess
import socket
import json
import time
import os
from functools import partial

HOSTFILE_IP_KEY = 'hostfile_ips'
HOSTFILE = 'hostfile.txt'
MPI_JOB_COMPLETE_VAR = "mpi_job_status"
PUBLIC_KEY_RECEIVED_VAR = "public_key_received"
CONTROL_TASK_DONE_PATH = 'control'
MPI_PUBLIC_KEY_PATH = 'public_keys'

class MPIExecutor:

    def __init__(self, hosts) -> None:
        self.hosts = [h for h in hosts if h != socket.gethostbyname(socket.gethostname())]
        self._scan_all_hosts()

    def _exec_cmd(self, exe, args, program=None, program_args=None):
        """
        `exe` : str - one of mpicc, mpirun, or mpiexec
        `args` : List[str] - arguments to pass to `exe`
        `program`: str - program to run, such as compiled binary or python script
        `program_args`: List[str] - arguments to pass after `program`

        full command structure is: `exe` `args` `program` `program_args`
        """

        cmd = [exe] 

        if args is not None:
            cmd.extend(args)
        else:
            raise ValueError("Either `args` must be provided.")

        if program is not None:
            cmd.extend(program.split())

        if program_args is not None:
            cmd.extend(program_args)
        
        print(" ".join(cmd)) # TODO: Remove this
        try:
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
                while process.poll() is None:
                    stdout = process.stdout.read1()
                    try:
                        text = stdout.decode("utf-8")
                    except UnicodeDecodeError:
                        # TODO: This print feels bad, maybe remove - even better, 
                        # figure out how to handle the edge decoding cases gracefully.
                        # print("UnicodeDecodeError, skipping decoding of problematic bytes: %s" % stdout)
                        text=''
                    
                    print(text, end='', flush=True)
                    # TODO (Eddie): what is strat for dynamic cards? stuff `text` somewhere?
        except subprocess.CalledProcessError as e:
            print(e.stdout)
            raise e

    def cc(self, args=None):
        self._exec_cmd("mpicc", args=args)
    
    def run(self, args=None, program=None, program_args=None):
        if "--hostfile" not in args:
            args.extend(["--hostfile", HOSTFILE])
        self._exec_cmd("mpirun", args=args, program=program, program_args=program_args)

    def exec(self, args=None, program=None, program_args=None):
        if "--hostfile" not in args:
            args.extend(["--hostfile", HOSTFILE])
        self._exec_cmd("mpiexec", args=args, program=program, program_args=program_args)

    def _scan_cmd(self, host):
        return ["ssh-keyscan", "-H", host]

    def _scan_all_hosts(self):
        for host in self.hosts:
            try: 
                result = subprocess.run(self._scan_cmd(host), stdout = subprocess.PIPE, stderr = subprocess.STDOUT, check=True)
                if result.returncode != 0:
                    raise Exception("Error adding host to known_hosts: " + result.stdout.decode('utf-8'))
                else:
                    with open(os.path.expanduser("~/.ssh/known_hosts"), 'a') as f:
                        f.write(result.stdout.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                print(e.stdout)
                raise e

    def _scp_cmd(self, host, filename):
        return ["scp", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=no", filename, "root@%s:/metaflow/" % host]

    def broadcast_file(self, filename):
        self._scan_all_hosts()
        for host in self.hosts:
            try:
                result = subprocess.run(self._scp_cmd(host, filename), stdout = subprocess.PIPE, stderr = subprocess.STDOUT, check=True,)
                if result.returncode != 0:
                    raise Exception("Error copying executable: " + result.stdout.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                print(e.stdout)
                raise e
    

class MPIDecorator(ParallelDecorator):

    name = "mpi"
    defaults = {"all_nodes_started_timeout": 90, "worker_polling_freq": 5}
    IS_PARALLEL = True

    # Is this an anti-pattern? 
    # Could not find a better way without modifying the base @kubernetes + @parallel implementation
    # based on MPI-like decorators that need passwordless ssh and to be running sshd as daemon.
    requires_passwordless_ssh = True

    def _setup_current(self, hosts):
        from metaflow import current
        current._update_env({"mpi" : MPIExecutor(hosts)})

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        from metaflow.plugins.kubernetes.kubernetes_decorator import KubernetesDecorator
        from metaflow.plugins.aws.batch.batch_decorator import BatchDecorator
        from metaflow.plugins.aws.aws_utils import compute_resource_attributes
        self.is_batch = False
        self.is_k8s = False
        self.is_local = False
        for deco in decos:
            if isinstance(deco, KubernetesDecorator):
                self.is_k8s = True
                break
            elif isinstance(deco, BatchDecorator):
                self.is_batch = True
                break
        else:
            self.local = True
        self.environment = environment
        for deco in decos:
            if deco.name in ['resources', 'kubernetes', 'batch']:
                compute_deco_attrs = compute_resource_attributes(decos, deco, {"cpu": "1", "gpu": "0"})
                try:
                    self.n_slots = int(compute_deco_attrs['gpu'])
                except KeyError:
                    self.n_slots = int(compute_deco_attrs['cpu'])
                if not self.n_slots > 0:
                    self.n_slots = int(compute_deco_attrs['cpu'])
                break

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        if self.is_k8s:
            self.jobset_name = "jobset-%s" % task_id.split('-')[-1]
        elif self.is_batch:
            raise NotImplementedError("AWS Batch is not implemented for MPI yet")

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):

        # TODO: Investigate better patterns for submitting step_func code on control node and looping the workers.
        # The pattern in this function works okfor running @ray_parallel, @mpi, @deepspeed, etc.
        # Seems there should be a better, more elegant way to not always run the same exact code in the @parallel context.
        # https://github.com/Netflix/metaflow/blob/d01ae37c03363be0289fbe02d10d26cf4fb3bc1b/metaflow/task.py#L571

        from metaflow import current, S3

        if not os.environ.get("METAFLOW_RUNTIME_ENVIRONMENT", "local") == "local":
            s3 = S3(run=flow)
            assert os.environ["OMPI_ALLOW_RUN_AS_ROOT"]=="1", "Please set OMPI_ALLOW_RUN_AS_ROOT=1 in your environment."
            assert os.environ["OMPI_ALLOW_RUN_AS_ROOT_CONFIRM"]=="1", "Please set OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 in your environment."

        def _worker_heartbeat(polling_freq=self.attributes["worker_polling_freq"], var=MPI_JOB_COMPLETE_VAR):
            control_done = False
            while not control_done:
                time.sleep(polling_freq)
                try:
                    control_done = json.loads(s3.get(CONTROL_TASK_DONE_PATH).blob)[var]
                except metaflow.plugins.datatools.s3.s3.MetaflowS3NotFound:
                    control_done = False
                    continue
                
        def _control_wrapper(step_func, flow, var=MPI_JOB_COMPLETE_VAR):
            step_func()
            s3.put(CONTROL_TASK_DONE_PATH, json.dumps({var: True}))

        def _empty_worker_task():
            pass

        if os.environ.get("METAFLOW_RUNTIME_ENVIRONMENT", "local") == "local":
            if ubf_context == UBF_CONTROL:
                env_to_use = getattr(self.environment, "base_env", self.environment)
                self._setup_current(["127.0.0.1"])
                return partial(
                    _local_multinode_control_task_step_func,
                    flow,
                    env_to_use, 
                    step_func,
                    retry_count,
                )
            return partial(_empty_worker_task)
        else:
            hosts = self.setup_distributed_env(flow, ubf_context, n_slots=self.n_slots)
            self._setup_current(hosts)
            if ubf_context == UBF_CONTROL:
                return partial(_control_wrapper, step_func=step_func, flow=flow)
            return partial(_worker_heartbeat)

    def setup_distributed_env(self, flow, ubf_context, n_slots=1):
        "Return a list of strings of hostnames of nodes to use for MPI"
        if self.is_k8s:
            return setup_mpi_kubernetes_env(flow, self.jobset_name, ubf_context, self.attributes["all_nodes_started_timeout"], self.attributes["worker_polling_freq"], n_slots)
        elif self.is_batch:
            raise NotImplementedError("AWS Batch is not implemented for MPI yet")


def setup_mpi_kubernetes_env(run, jobset_service_name, ubf_context, all_nodes_started_timeout, interval, n_slots):

    from metaflow import current, S3
    s3 = S3(run=run)

    world_size = int(os.environ["WORLD_SIZE"])
    if ubf_context == UBF_CONTROL:
        node_index = 0
        key_push_path = "%s/control" % (MPI_PUBLIC_KEY_PATH)
    else:
        node_index = int(os.environ["RANK"]) + 1
        key_push_path = "%s/worker/%s" % (MPI_PUBLIC_KEY_PATH, node_index)

    if not os.path.exists("/usr/sbin/sshd"):
        msg = "sshd not found in container. Please install openssh-server in the image used in a step with @mpi."
        raise MetaflowException(msg)

    ssh_dir = os.path.expanduser("~/.ssh")
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)
    os.chmod(ssh_dir, 0o700)

    # Generate host key
    result = subprocess.run(
        ["ssh-keygen", "-t", "rsa", "-f", os.path.join(ssh_dir, "id_rsa"), '-N', ''], 
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        check=True
    )
    assert result.returncode == 0, "Error generating host key"

    # Move public key to S3
    with open(os.path.join(ssh_dir, "id_rsa.pub"), 'r') as f:
        s3.put(key_push_path, f.read())

    if ubf_context == UBF_CONTROL:
        
        # loop until all workers have pushed their public keys
        worker_keys_path = "%s/worker" % MPI_PUBLIC_KEY_PATH
        while True:
            try:
                paths = s3.list_paths([worker_keys_path])
                if len(paths) == world_size - 1: # all nodes minus control
                    break
                time.sleep(interval)
            except metaflow.plugins.datatools.s3.s3.MetaflowS3NotFound:
                time.sleep(interval)
                continue
        
        # append all public keys to authorized_keys file
        with open(os.path.join(ssh_dir, "authorized_keys"), 'a') as g:
            for p in paths:
                tail = p.url.split(MPI_PUBLIC_KEY_PATH)[-1][1:]
                obj = s3.get(os.path.join(MPI_PUBLIC_KEY_PATH, tail))
                g.write(obj.text)

    else:
        control_key_path = "%s/control" % MPI_PUBLIC_KEY_PATH
        while True:
            try:
                obj = s3.get(control_key_path)
                with open(os.path.join(ssh_dir, "authorized_keys"), 'a') as g:
                    g.write(obj.text)
                break
            except metaflow.plugins.datatools.s3.s3.MetaflowS3NotFound:
                time.sleep(interval)
                continue
    os.chmod(os.path.join(ssh_dir, "authorized_keys"), 0o600)

    # enable passwordless ssh
    ssh_config_options = [
        "PubKeyAuthentication yes",
        "RSAAuthentication yes" # TODO: can this be removed?
    ]
    with open('/etc/ssh/sshd_config', 'a') as f:
        f.write('\n'.join(ssh_config_options))
    result = subprocess.run(["sudo", "service", "ssh", "restart"], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.returncode == 0, "Error restarting sshd"

    node_index = int(os.environ["RANK"])
    if ubf_context != UBF_CONTROL:
        node_index += 1
    num_nodes = int(os.environ["WORLD_SIZE"])
    my_ip = socket.gethostbyname(socket.gethostname())
    username = subprocess.run(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.decode('utf-8').strip()

    # Share IPs to write the hosts file
    s3.put("%s/%s" % (HOSTFILE_IP_KEY, node_index), my_ip)
    while True: 
        s3_hostfile_entry_paths = s3.list_paths([HOSTFILE_IP_KEY])
        if len(s3_hostfile_entry_paths) == num_nodes:
            hosts = [
                s3.get(os.path.join(*s3obj.url.split('/')[-2:])).blob.decode('utf-8')
                for s3obj in s3_hostfile_entry_paths
            ]
            break
        time.sleep(5)

    with open(HOSTFILE, 'a') as f:
        for h in hosts:
            if h == my_ip:
                h = "127.0.0.1"
            f.write("%s slots=%s\n" % (h, n_slots))

    s3.close()
    return hosts

STEP_DECORATORS_DESC = [("mpi", ".MPIDecorator")]