import unittest

from sapiopylib.rest.utils.recordmodel.RecordModelManager import RecordModelManager

from sapiopylib.rest.DataMgmtService import DataMgmtServer

from sapiopylib.rest.utils.recordmodel.PyRecordModel import PyRecordModel

from sapiopylib.rest.utils.FoundationAccessioning import FoundationAccessionManager

from sapiopylib.rest.User import SapioUser

user = SapioUser(url="https://linux-vm:8443/webservice/api", verify_ssl_cert=False,
                 guid="3c232543-f407-4828-aae5-b33d4cd31fa7",
                 username="yqiao_api", password="Password1!")
data_record_manager = DataMgmtServer.get_data_record_manager(user)
eln_manager = DataMgmtServer.get_eln_manager(user)
rec_man = RecordModelManager(user)
inst_man = rec_man.instance_manager

# Note: this should be run, then create some samples in real ELN not in python, and then run this again, then ELN again.
class TestPR51537(unittest.TestCase):
    def test_accessioning_again(self):
        accessioning: FoundationAccessionManager = FoundationAccessionManager(user)
        sample_list_1: list[PyRecordModel] = inst_man.add_new_records("Sample", 5)
        sample_id_list_1: list[str] = accessioning.get_accession_with_config_list("Sample", "SampleId", 5)
        for sample, sample_id in zip(sample_list_1, sample_id_list_1):
            sample.set_field_value("SampleId", sample_id)
        sample_list_2: list[PyRecordModel] = inst_man.add_new_records("Sample", 5)
        sample_id_list_2: list[str] = accessioning.get_accession_with_config_list("Sample", "SampleId", 5)
        for sample, sample_id in zip(sample_list_2, sample_id_list_2):
            sample.set_field_value("SampleId", sample_id)
        for sample_id in sample_id_list_2:
            for previous_id in sample_id_list_1:
                self.assertTrue(sample_id > previous_id)
        rec_man.store_and_commit()


if __name__ == '__main__':
    unittest.main()
