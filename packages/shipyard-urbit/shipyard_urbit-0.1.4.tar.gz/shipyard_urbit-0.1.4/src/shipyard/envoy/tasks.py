from multiprocessing import active_children, get_context
from shipyard.envoy.tunnel import open_tunnel
from shipyard.models import SshTunnel, Task


class TunnelTask(Task):
    ssh: SshTunnel

    def job_name(self):
        url = self.ssh.url
        remote = self.ssh.remote_port
        local = self.ssh.local_port
        return f"tunnel;{url};{remote};{local}"


class OpenTunnelTask(TunnelTask):
    version = 1

    def run(self):
        process = get_context("spawn").Process(
            target=open_tunnel,
            name=self.job_name(),
            args=(self.ssh,),
            daemon=True,
        )
        process.start()


class CloseTunnelTask(TunnelTask):
    version = 1

    def run(self):
        for p in active_children():
            if p.name == self.job_name():
                p.terminate()
                p.join()
