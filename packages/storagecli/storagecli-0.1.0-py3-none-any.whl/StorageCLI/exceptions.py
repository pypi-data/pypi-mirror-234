import click
import requests


def check_response_for_error(response: requests.Response):
    match response.status_code:
        case 200 | 201:
            pass
        case 403 | 404 | 422 | 410 | 503 | 500:
            try:
                detail = (response.json().get("detail")
                          .replace("Tenant", "Organization").replace("tenant", "organization"))
            except:
                detail = response.content
            raise click.ClickException(f"{response.status_code}\n"
                                       f"{detail}")
        case _:
            pass
