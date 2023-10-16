import psycopg2
import requests

class Quill:
    def __init__(
        self,
        private_key,
        database_connection_string,
    ):
        self.private_key = private_key
        self.database_connection_string = database_connection_string
        self.main_pool = psycopg2.connect(database_connection_string)

    def query(self, org_id, data):
        metadata = data["metadata"]
        
        target_pool = self.main_pool
        task = metadata["task"]

        headers = {"Authorization": f"Bearer {self.private_key}"}

        if task == "query":
            try:
                url = "https://quill-344421.uc.r.appspot.com/validate"
                headers = {
                    "Authorization": f"Bearer {self.private_key}",
                }
                params = {
                    "orgId": org_id,
                }
                response = requests.post(
                    url, json={"query": metadata.get("query")}, headers=headers, params=params
                )
                response_data = response.json()
                field_to_remove = response_data.get("fieldToRemove")

                cursor = target_pool.cursor()
                cursor.execute(response_data["query"])
                query_result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                formatted_result = {
                    "fields": [col for col in columns if col != field_to_remove],
                    "rows": [dict(zip(columns, row)) for row in query_result],
                }

                # Remove the undesired field from the row dictionaries
                for row in formatted_result["rows"]:
                    if field_to_remove in row:
                        del row[field_to_remove]

                return formatted_result

            except Exception as err:
                return {"error": str(err), "errorMessage": str(err) if err else ""}

        elif task == "config":
            try:
                response = requests.get(
                    "https://quill-344421.uc.r.appspot.com/config",
                    params={
                        "orgId": org_id,
                        "name": metadata.get("name")
                    },
                    headers={
                        "Authorization": f"Bearer {self.private_key}",
                    },
                )
                dash_config = response.json()

                if dash_config and dash_config["filters"]:
                    for i, filter in enumerate(dash_config["filters"]):
                        # run query
                        cursor = target_pool.cursor()
                        cursor.execute(filter["query"])
                        rows = cursor.fetchall()

                        # Update the options for each filter with the rows
                        dash_config["filters"][i]["options"] = rows

                return dash_config
            
            except Exception as err:
                return {"error": str(err), "errorMessage": str(err) if err else ""}

        elif task == "create":
            try:
                response = requests.post(
                    "https://quill-344421.uc.r.appspot.com/item",
                    json=metadata,
                    params={"orgId": org_id},
                    headers=headers,
                ).json()

                return response
            except:
                return {"error": str(err), "errorMessage": str(err) if err else ""}

        elif task == "item":
            try:
                resp = requests.get(
                    "https://quill-344421.uc.r.appspot.com/selfhostitem",
                    params={"id": metadata.get("id"), "orgId": org_id},
                    headers={"Authorization": f"Bearer {self.private_key}"},
                )
                resp_data = resp.json()
                data_to_send = {
                "query": resp_data["queryString"],
                "orgId": org_id,
                "filters": metadata.get("filters")
                }

                response = requests.post(
                    "https://quill-344421.uc.r.appspot.com/validate",
                    json=data_to_send,
                    headers={"Authorization": f"Bearer {self.private_key}"}
                )
                response_data = response.json()
                

                field_to_remove = response_data["fieldToRemove"] if response_data["fieldToRemove"] else None

                with target_pool.cursor() as cursor:
                    cursor.execute(response_data["query"])
                    query_result = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    rows = [dict(zip(columns, row)) for row in query_result]
                    fields = [column for column in columns if column != field_to_remove]
                    rows = [
                        {
                            key: value
                            for key, value in row.items()
                            if key != field_to_remove
                        }
                        for row in rows
                    ]

                return {**resp_data, "fields": fields, "rows": rows}

            except Exception as err:
                return {"error": str(err), "errorMessage": str(err) if err else ""}