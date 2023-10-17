import time

from talkytimes.base import AbstractAutomation


class TalkyTimesAutomation(AbstractAutomation):

    def save_users(self, *, min_value: int, max_value: int):
        page = min_value
        service = "/platform/account/search"
        body = {"filters": {"ageTo": 90, "ageFrom": 18, "gender": None},
                "limit": 100}
        while page < max_value:
            body["page"] = page
            try:
                response = self.driver.execute_script(
                    script=self.get_script(service=service, body=body)
                )
                data = response.get("data")
                users = data.get("users")
                if not len(users) > 0:
                    break
                for user in users:
                    try:
                        self.db.create_or_update(
                            profile_id=self.profile_id,
                            external_id=str(user.get("id")),
                            status=user.get("is_online")
                        )
                        time.sleep(1)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
            page += 1
        print("Finished")

    def save_users_chat(self, *, min_value: int, max_value: int):
        users = self.db.get_users(profile_id=self.profile_id)
        count = min_value
        for user in users[min_value:max_value]:
            external_id = user.get("external_id")
            service = f"/platform/chat/restriction?idRegularUser={external_id}"
            try:
                response = self.driver.execute_script(
                    script=self.get_script(service=service)
                )
                data = response.get("data")
                if data:
                    self.db.update_user(
                        id=user.get("id"),
                        item=dict(
                            messages=str(data.get("messagesLeft")),
                            emails=str(data.get("lettersLeft"))
                        )
                    )
            except Exception as e:
                print(e)
            count += 1
            time.sleep(1)
        print("Finished")

    def like_follow(self, *, min_value: int, max_value: int):
        users = self.db.get_users(profile_id=self.profile_id)
        count = min_value
        for user in users[min_value:max_value]:
            external_id = user.get("external_id")
            like_service = f"/platform/social-action/like"
            follow_service = f"/platform/social-action/follow"
            body = {"idInterlocutor": int(external_id)}
            try:
                self.driver.execute_script(
                    script=self.get_script(service=like_service, body=body)
                )
                time.sleep(1)
                self.driver.execute_script(
                    script=self.get_script(service=follow_service, body=body)
                )
            except Exception as e:
                print(e)
            count += 1
            time.sleep(1)
        print("Finished")
