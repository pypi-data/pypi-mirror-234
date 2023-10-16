#-*- coding: utf-8 -*-
import os #내장모듈
import datetime #내장모듈

import pynal  # xython 모듈
import basic_data  # xython 모듈

import win32com.client #pywin32의 모듈

class mailmail:
    def __init__(self):
        self.base_mail = win32com.client.dynamic.Dispatch('Outlook.Application')
        self.outlook = self.base_mail.GetNamespace("MAPI")
        self.sigan = pynal.pynal()

        self.base_data = basic_data.basic_data()
        self.var = self.base_data.vars
        self.var_common = {}


    def check_outlook_email_test(self):
        # 테스트를 위한것

        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        input_folder = namespace.GetDefaultFolder(6)
        # print("폴더이름 ==> ", input_folder.Name)

        for i in input_folder.items:
            print(i.subject)
            print(str(i.Sender) + '\t: ' + i.SenderEmailAddress)

        print("전체 메일 개수 :" + str(input_folder.items.count))
        print("읽지않은 메일 개수 :" + str(input_folder.UnReadItemCount))
        print("읽은 메일 개수 :" + str(input_folder.items.count - input_folder.UnReadItemCount))

        print(namespace.Folders[0].Name)
        print(namespace.Folders[1].Name)
        print(namespace.Folders[2].Name)

        root_folder = namespace.Folders.Item(1)
        for folder in root_folder.Folders:
            print("폴더이름 ==> ", folder.Name)
            print("갯수 ==> ", folder.items.count)

        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        root_folder = namespace.Folders.Item(1)
        subfolder = root_folder.Folders['All'].Folders['Main Folder'].Folders['Subfolder']
        messages = subfolder.Items

    def data_all_properties_names_for_mail(self):
        result = ["Actions",
                  "AlternateRecipientAllowed",
                  "Application",
                  "Attachments",
                  "AutoForwarded",
                  "AutoResolvedWinner",
                  "BCC",
                  "BillingInformation",
                  "Body",
                  "BodyFormat",
                  "Categories",
                  "CC",
                  "Class",
                  "Companies",
                  "Conflicts",
                  "ConversationID",
                  "ConversationIndex",
                  "ConversationTopic",
                  "CreationTime",
                  "DeferredDeliveryTime",
                  "DeleteAfterSubmit",
                  "DownloadState",
                  "EntryID",
                  "ExpiryTime",
                  "FlagRequest",
                  "FormDescription",
                  "GetInspector",
                  "HTMLBody",
                  "Importance",
                  "InternetCodepage",
                  "IsConflict",
                  "IsMarkedAsTask",
                  "ItemProperties",
                  "LastModificationTime",
                  "MarkForDownload",
                  "MessageClass",
                  "Mileage",
                  "NoAging",
                  "OriginatorDeliveryReportRequested",
                  "OutlookInternalVersion",
                  "OutlookVersion",
                  "Parent",
                  "Permission",
                  "PermissionService",
                  "PermissionTemplateGuid",
                  "PropertyAccessor",
                  "ReadReceiptRequested",
                  "ReceivedByEntryID",
                  "ReceivedByName",
                  "ReceivedOnBehalfOfEntryID",
                  "ReceivedOnBehalfOfName",
                  "ReceivedTime",
                  "RecipientReassignmentProhibited",
                  "Recipients",
                  "ReminderOverrideDefault",
                  "ReminderPlaySound",
                  "ReminderSet",
                  "ReminderSoundFile",
                  "ReminderTime",
                  "RemoteStatus",
                  "ReplyRecipientNames",
                  "ReplyRecipients",
                  "RetentionExpirationDate",
                  "RetentionPolicyName",
                  "RTFBody",
                  "Saved",
                  "SaveSentMessageFolder",
                  "Sender",
                  "SenderEmailAddress",
                  "SenderEmailType",
                  "SenderName",
                  "SendUsingAccount",
                  "Sensitivity",
                  "Sent",
                  "SentOn",
                  "SentOnBehalfOfName",
                  "Session",
                  "Size",
                  "Subject",
                  "Submitted",
                  "TaskCompletedDate",
                  "TaskDueDate",
                  "TaskStartDate",
                  "TaskSubject",
                  "To",
                  "ToDoTaskOrdinal",
                  "UnRead",
                  "UserProperties",
                  "VotingOptions",
                  "VotingResponse"]
        return result

    def get_10_latest_mail_data_in_default_input_folder(self):
        # 최신 10개의 메일 정보를 갖고오는 것
        result = self.get_latest_mail_data_in_default_input_folder_by_limit_no(10)
        return result

    def get_10_latest_mails(self):
        # 받은편지함에서 최근 10개의 메일을 돌려받는것
        result = []
        many_mail = self.get_latest_mail_items_at_input_mail_box(10)
        for num in range(len(many_mail)):
            temp = self.get_one_mail_information(many_mail[num])
            result.append(temp)
        return result

    def get_all_default_folder_information(self):
        result = []
        for no in range(0, 50):
            try:
                temp = self.outlook.GetDefaultFolder(no)
                result.append([no, temp.name])
            except:
                pass
        return result

    def get_all_information_for_one_mail(self, input_mail):
        result = {}
        result["sender"] = input_mail.SenderName
        result["time"] = input_mail.ReceivedTime
        result["receiver"] = input_mail.To
        result["title"] = input_mail.Subject
        result["body"] = input_mail.Body
        return result

    def get_all_mail_information_for_mail_box_by_limit(self, input_mail_box, limit_no=0):
        # 폴더 객체안의 모든 메세지에대한 정보를 리스트+사전 형태로 만든다
        result = []
        messages = input_mail_box.Items
        messages.Sort("ReceivedTime", True)
        message = messages.GetFirstO
        total_no = 1
        for no in range(input_mail_box.items.count):
            temp = self.get_all_information_for_one_mail(message)
            message = messages.GetNextO
            result.append(temp)
            if limit_no:
                if limit_no == total_no:
                    break
            total_no = total_no + 1
        return result

    def get_all_mails_in_mail_box(self, input_mail_box):
        messages = input_mail_box.Items
        return messages

    def get_attached_filename_all_for_one_mail(self, input_mail):
        # 이메일 안에 들어있는 첨부화일의 이름들 알아보기
        result = []
        attachments = input_mail.Attachments
        num_attach = len([x for x in attachments])
        if num_attach > 0:
            for x in range(1, num_attach + 1):
                attachment = attachments.Item(x)
                result.append(attachment.FileName)
        return result

    def get_basic_draft_folder(self):
        # 기본적인 보낸 편지함
        input_folder = self.outlook.GetDefaultFolder(16)
        return input_folder

    def get_basic_input_folder(self):
        # 기본적인 받은 편지함
        input_folder = self.outlook.GetDefaultFolder(6)
        return input_folder

    def get_basic_promise_folder(self):
        # 기본적인 보관함 폴더
        input_folder = self.outlook.GetDefaultFolder(9)
        return input_folder

    def get_each_mail_in_mail_box_by_limit_no(self, input_mail_box, limit_no=5):
        # 폴더객체안의 날짜기준으로 최근에 들어온 몇개의 메세지만 갖고오는것
        messages = input_mail_box.Items
        messages.Sort("ReceivedTime", True)
        result = list(messages)[:limit_no]
        return result

    def get_each_mail_information_for_mails(self, input_mails):
        result = []
        for message in input_mails:
            temp = self.get_all_information_for_one_mail(message)
            result.append(temp)
        return result

    def get_latest_mail_data_in_default_input_folder_by_limit_no(self, input_no=10):
        # 기본 입력 폴더의 최근 갯수의 메일 자료를 갖고온다
        result = []
        input_folder = self.outlook.GetDefaultFolder(6)
        messages = input_folder.Items
        message = messages.GetFirstO
        num = 1
        for no in range(input_no):
            result.append(self.get_all_information_for_one_mail(message))
            if num == input_no:
                break
            else:
                num = num + 1
                message = messages.GetNextO
        return result

    def get_latest_mail_items_at_input_mail_box(self, input_no=5):
        result = []
        input_folder = self.outlook.GetDefaultFolder(6)
        messages = input_folder.Items
        messages.Sort("ReceivedTime", True)
        message = messages.GetFirst()

        for no in range(input_no):
            print(message.Subject)
            message = messages.GetNext()
            result.append(message)
        return result

    def get_mail_box_by_default_index_no(self, default_index_no=6):
        result = self.outlook.GetDefaultFolder(default_index_no)
        return result

    def get_mail_box_by_folder_index(self, top_folder_index=0):
        # top 폴더의 index 와
        # 원하는 폴더 번호를 넣으면 폴더 객체를 돌려준다
        result = self.outlook.Folders[top_folder_index]
        return result

    def get_mail_box_by_sub_folder_name(self, top_folder_name="", sub_folder_name=""):
        # top 폴더의 index 와 원하는 폴더 번호를 넣으면 폴더 객체를 돌려준다
        top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
        sub_folder_index = self.get_sub_folder_index_by_folder_name(top_folder_index, sub_folder_name)
        result = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
        return result

    def get_mail_box_by_sub_folder_name_only(self, input_folder_name=""):
        # 폴더이름으로 폴더 객체를 만들고 확인하는 것
        result = self.get_mail_box_for_default_input_folder()
        if input_folder_name != "":
            temp = []
            top_folder_data = self.get_top_folder_name_all()
            for top_1 in top_folder_data:
                sub_folder_data = self.read_sub_folder_name_all_in_folder_name(top_1[1])
                for sub_1 in sub_folder_data:
                    if sub_1[2] == input_folder_name:
                        result = self.get_mail_box_by_sub_folder_name(sub_1[0], sub_1[2])
                        break
        return result

    def get_mail_box_by_top_n_sub_folder_index(self, top_folder_index=0, sub_folder_index=6):
        # 폴더의 이름으로 찾는것
        result = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
        return result

    def get_mail_box_for_default_input_folder(self):
        result = self.outlook.GetDefaultFolder(6)
        return result

    def get_mail_box_of_default_draft_folder(self):
        # 임시보관함
        folder = self.outlook.GetDefaultFolder(16)
        return folder

    def get_mail_box_of_default_promise_folder(self):
        folder = self.outlook.GetDefaultFolder(9)
        return folder

    def get_mail_items_in_folder(self, folder_object, input_no=5):
        result = []
        messages = folder_object.Items
        messages.Sort("ReceivedTime", True)
        message = messages.GetFirst()

        for no in range(input_no):
            print(message.Subject)
            message = messages.GetNext()
            result.append(message)
        return result

    def get_mails_in_mail_box_by_from_to(self, input_mail_box, from_no=0, to_no=25):
        # 폴더객체안의 날짜기준으로 최근에 들어온 몇개의 메세지만 갖고오는것
        messages = input_mail_box.Items
        messages.Sort("ReceivedTime", True)
        result = list(messages)[from_no:to_no]
        return result

    def get_new_mails_on_today_in_default_input_folder(self):
        # 받은편지함의 자료를 읽어서 새로운것만 제목보여주기
        items = self.get_unread_mails_in_default_input_folder()
        item_data_list2d = self.get_each_mail_information_for_mails(items)
        for one in item_data_list2d:
            print(one)

    def get_nos_of_mails_in_mail_box(self, mail_box):
        # 폴더객체안의 메일 갯수
        result = mail_box.items.count
        return result

    def get_nos_of_unread_mails_in_mail_box(self, mail_box):
        # 폴더객체안의 읽지않은 메일 갯수 확인
        # input_folder = mail.box.items.count
        temp_item = mail_box.Items.Restricts("[Unread] =true")
        result = temp_item.count
        return result

    def get_one_mail_information(self, one_email):
        result = {}
        result["sender"] = one_email.SenderName
        result["receiver"] = one_email.To
        result["title"] = one_email.Subject
        result["time"] = one_email.ReceivedTime
        result["body"] = one_email.Body
        return result

    def get_sub_folder_index_by_folder_name(self, top_folder_name="", sub_folder_name=""):
        # 폴더이름으로 폴더 객체를 만들고 확인하는 것
        top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
        result = ""
        if type(sub_folder_name) == type(123):
            result = sub_folder_name
        else:
            sub_folder_data = self.read_sub_folder_name_all_in_folder_name(top_folder_index)
            for sub_1 in sub_folder_data:
                if sub_1[2] == sub_folder_name:
                    result = sub_1[1]
                    break
        return result

    def get_sub_folders_names(self, folder_name):
        result = []
        for no in range(self.outlook.Folders[folder_name].Folders.count):
            this_name = self.outlook.Folders[folder_name].Folders[no].name
            result.append([folder_name, no, this_name])
        return result

    def get_top_folder_index_by_folder_name(self, folder_name=""):
        # 폴더이름을 입력하면 index 를 돌려주는것
        result = folder_name
        if type(folder_name) != type(123):
            top_folder_data = self.get_top_folder_name_all()
            for top_1 in top_folder_data:
                if top_1[1] == folder_name:
                    result = top_1[0]
                    break
        return result

    def get_top_folder_name_all(self):
        # 제일위의 폴더를 갖고온다
        result = []
        for no in range(self.outlook.Folders.count):
            this_name = self.outlook.Folders[no].Name
            result.append([no, this_name])
        return result

    def get_top_folder_names(self):
        result = []
        for no in range(self.outlook.Folders.count):
            this_name = self.outlook.Folders[no].Name
            result.append([no, this_name])
        return result

    def get_total_mail_no_at_folder(self, folder_name):
        result = self.outlook.Folders[folder_name].Folders.items.count
        return result

    def get_unread_mails_in_default_input_folder(self):
        # 기본 받은 편지함의 읽지 않은 메일을 객체로 돌려준다
        input_folder = self.outlook.GetDefaultFolder(6)
        result = input_folder.Items.Restrict("[Unread]=true")
        return result

    def get_unread_mails_in_mail_box(self, input_mail_box):
        # 입력한 폴데객체의 읽지 않은 메일을 객체로 돌려준다
        result = input_mail_box.Items.Restrict("[Unread] =true")
        return result

    def get_unread_mails_information_in_default_input_folder(self):
        # 받은편치함의 자료를 읽어서 새로운것만 제목보여주기
        items = self.get_unread_mails_in_default_input_folder()
        item_data_list2d = self.get_each_mail_information_for_mails(items)
        return item_data_list2d

    def manual(self):
        result = """ 
        top folder: 제일위의 폴더
        item : 한개 메세지에 대한 정보와 메소드틀 갖고있는 클래스 객체 """

    def manual_mail(self):
        new_mail = self.base_mail.Createltem(0)
        print(new_mail)

    def move_mails_to_target_mail_box(self, input_mails, target_mail_box):
        # 메일 객체를 다른 폴더로 옮기는 것
        for message in input_mails:
            message.Move(target_mail_box)

    def read_basic_input_mails_data_with_outlook(self):
        input_folder = self.outlook.GetDefaultFolder(6)
        for message in input_folder.Items:
            print(message.Subject)

    def read_sub_folder_name_all_in_folder_name(self, input_folder_name):
        # top 폴더의 하위폴더들의 이름을 돌려주는 것
        top_folder_index = self.get_top_folder_index_by_folder_name(input_folder_name)
        result = []
        for no in range(self.outlook.Folders[top_folder_index].Folders.count):
            this_name = self.outlook.Folders[top_folder_index].Folders[no].name
            result.append([input_folder_name, no, this_name])
        return result

    def read_total_unread_mail_no_with_outlook(self, folder_name):
        input_folder = self.outlook.Folders[folder_name].Folders.items.count
        result = input_folder.UnReadItemsCount
        return result

    def read_unread_mail_from_basic_input_folder_with_outlook(self):
        input_folder = self.outlook.GetDefaultFolder(6)
        for message in input_folder.Items.Restrict("Unread]=true"):
            print(message.Subject)

    def save_attached_file_for_one_mail(self, input_mail, path="", surname="", new_name=""):
        # 이메일 안에 들어있는 첨부화일을 다른 이름으로 저장하기
        # path : 저장할 경로，없으면 현재의 위치
        # surname : 기존이름앞에 붙이는 목적，없으면 그대로
        # new_name : 새로운 이름으로 변경
        attachments = input_mail.Attachments
        num_attach = len([x for x in attachments])
        if num_attach > 0:
            for x in range(1, num_attach + 1):
                attachment = attachments.Item(x)
                old_name_changed = surname + attachment.FileName
                if new_name:
                    old_name_changed = new_name
                    attachment.SaveAsFile(os.path.join(path, old_name_changed))

    def send_mail_with_outlook(self, input_dic):
        new_mail = self.outlook.CreateItem(0)
        new_mail.To = input_dic["to"]
        new_mail.Subject = input_dic["subject"]
        new_mail.Body = input_dic["body"]
        # attachment = "첨부화일들"
        # new_mail.Attachments.Add(attachment)
        new_mail.Send()

    def send_new_mail(self, to, subject="", body="", attachments=None):
        new_mail = self.base_mail.CreateItem(0)
        new_mail.To = to
        new_mail.Subject = subject
        new_mail.Body = body
        if attachments:
            for num in range(len(attachments)):
                new_mail.Attachments.Add(attachments[num])
        new_mail.Send()

    def send_new_mail_by_dic_type(self, input_dic):
        # 사전형식으로된 자료를 송부하는 것
        new_mail = self.base_mail.CreateItem(0)
        new_mail.To = input_dic["To"]
        new_mail.Subject = input_dic["Subject"]
        new_mail.Body = input_dic["Body"]
        if "Attachments" in input_dic.keys():
            attachment = input_dic["Attachments"]
            new_mail.Attachments.Add(attachment)
        new_mail.Send()

    def version(self):
        result = """ 2023-04-10 : 이름을 포함한, 많은 부분을 고침
        default folder: outlook 에서 기본으로 설정되고 관리되는 기준의 폴더들
        아웃룩의 메일은 item 과 folder 로 구성이 되어있다"""
        return result

    def get_mail_obj_in_mail_box_between_date(self, input_mail_box, dt_obj_from, dt_obj_to):
        # 날짜사이의 메일 객체들을 갖고오는것
        dt_obj_from = self.sigan.change_any_time_to_dt_obj(dt_obj_from)
        dt_obj_to = self.sigan.change_any_time_to_dt_obj(dt_obj_to)
        # 끝날묘포함하려면, 1 일을 더 더해줘야한다 #즉，2023-1-1 일 0 시 0 분 0 초를 넣어주는것과 같으므로, 2023-01-02 일 0 시 0 분 0 초로 하면 1 월 1 일의 모든 자료가 다 확인되는 것이다
        dt_obj_to = dt_obj_to + datetime.timedelta(days=1)
        # 폴더객체안의 받은 날짜사이에 들어온 메세지만 갖고오는것
        messages = input_mail_box.Items
        # 제일 최근에 받은즉，제일 받은시간이 늦은것을 기준으로 정렬
        messages.Sort("ReceivedTime", True)
        print(dt_obj_from.strftime("%m/%d/%Y %H:%M %p"))
        result = messages.Restrict("[ReceivedTime] >= '" + dt_obj_from.strftime(
            "%m/%d/%Y %H:%M %p") + "' AND [ReceivedTime] 〈= '" + dt_obj_to.strftime("%m/%d/%Y %H:%M %p") + "'")
        return result

    def get_mail_obj_in_mail_box_from_index_day(self, input_mail_box, input_no):
        # 몇일전까지의 메일을 갖고오는것
        dt_obj_to = self.sigan.get_today_as_dt_obj()
        # 끝날포포함하려면, 1 일을 더 더해줘야한다
        # 즉, 2023-1-1 일 0 시 0 분 0 초를 넣어주는것과 같으므로, 2023-01-02 일 0 시 0 분 0 초로 하면 1 월 1 일의 모든 자료가 다 확인되는 것이다
        dt_obj_from = dt_obj_to - datetime.timedelta(days=input_no - 1)
        # 폴더객체안의 받은 날짜사이에 들어온 메세지만 갖고오는것
        messages = input_mail_box.Items
        # 제일 최근에 받은것, 즉, 제일 받은시간이 늦은것을 기준으로 정렬
        messages.Sort("ReceivedTime", True)
        result = messages.Restrict("[ReceivedTime] >=	'" + dt_obj_from.strftime('%m/%d/%Y %H:%M %p') + "'")
        return result

    # 입력된 메일들중에 읽지 않은 것을 돌려준다
    def get_unread_mails_in_mails(self, messages):
        # 메교I지중에'읽지않호 4일을 돌려중
        result = messages.Restrict("[Unread] =true")
        return result

    def get_mail_box_by_top_n_sub_folder_name(self, top_folder_name="", sub_folder_name=""):
        # top 폴더와 서브폴더이름으로 폴더 객체를 갖고온다
        top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
        sub_folder_index = self.get_sub_folder_index_by_folder_name(top_folder_index, sub_folder_name)
        result = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
        return result

    def make_new_empty_mail(self):
        # 빈 메일객체를 하나 만든것
        new_mail = self.base_mail.CreateItem(0)
        new_mail.To = "to"
        new_mail.Subject = "subject"
        new_mail.Body = "body"
        return new_mail

    ##########################################################################

    def get_mail_datas_for_one_mail_item(self, input_mail_item):
        result = {}
        result["sender"] = input_mail_item["SenderName"]
        result["receiver"] = input_mail_item["To"]
        result["title"] = input_mail_item["Subject"]
        result["time"] = input_mail_item["ReceivedTime"]
        result["body"] = input_mail_item["Body"]
        return result

    def send_mail_item(self, input_dic):
        new_mail = self.base_mail.CreateItem(0)
        new_mail.To = input_dic["To"]
        new_mail.Subject = input_dic["Subject"]
        new_mail.Body = input_dic["Body"]
        if "Attachments" in input_dic.keys():
            attachment = input_dic["Attachments"]
            new_mail.Attachments.Add(attachment)
        new_mail.Send()

    def make_new_mail_for_draft_folder(self, **dic):
        # 빈 임시보관함으로 보내는 메일객체를 하나 만든것
        promise_folder = self.outlook.GetDefaultFolder(16)
        new_mail = self.base_mail.CreateItem(0)
        new_mail.To = dic["to"]
        new_mail.Subject = dic["subject"]
        new_mail.HTMubody = dic["body"]
        new_mail.Move(promise_folder)

    def get_selected_mails(self):
        # 아웃룩에서 어떤때를 보면, 선택한 자료를 확인할 필요가 있다
        # 이럴때 사용하기 힘든 것이다
        result = self.base_mail.ActiveExploer().Selection
        return result

    def make_draft_new_mail(self, **dic):
        # 빈 메일객체를 하나 만든것
        promise_folder = self.outlook.GetDefaultFolder(16)
        new_mail = self.base_mail.CreateItem(0)
        new_mail.To = dic["to"]
        new_mail.Subject = dic["subject"]
        new_mail.HTMLbody = dic["body"]
        print(dic["to"], dic["subject"], dic["body"])
        new_mail.Move(promise_folder)