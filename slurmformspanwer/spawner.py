from batchspawner import SlurmSpawner

from . form import SlurmSpawnerForm

class FakeMultiDict(dict):
    getlist = dict.__getitem__

class SlurmFormSpawner(SlurmSpawner):
    exec_prefix = ""
    batch_submit_cmd = "sudo -E -u {username} sbatch --parsable"
    batch_cancel_cmd = "sudo -u {username} scancel {jobid}"
    submit_path = '/etc/jupyterhub/submit.sh'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = SlurmSpawnerForm(self.user.name)

    @property
    def options_form(self):
        return self.form.render()

    def options_from_form(self, options):
        self.form.process(formdata=FakeMultiDict(options))
        return self.form.data

    @property
    def batch_script(self):
        with open(self.submit_path, 'r') as script_template:
            script = script_template.read()
        return script
