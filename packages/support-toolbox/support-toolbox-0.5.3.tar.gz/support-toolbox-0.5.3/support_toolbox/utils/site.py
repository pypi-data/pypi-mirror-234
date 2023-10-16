import requests
import json

SAML_PLACEHOLDER = {
    "entity_id": "http://www.okta.com/placeholder",
    "sso_url": "https://dev-placeholder.okta.com/app/placeholder/sso/saml",
    "x509_cert": """-----BEGIN CERTIFICATE-----
                MIIDqDCCApCgAwIBAgIGAYDyMs9qMA0GCSqGSIb3DQEBCwUAMIGUMQswCQYDVQQGEwJVUzETMBEG
                A1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsGA1UECgwET2t0YTEU
                MBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGRldi0xNjk5NDUxNzEcMBoGCSqGSIb3DQEJ
                ARYNaW5mb0Bva3RhLmNvbTAeFw0yMjA1MjMxODMzMTdaFw0zMjA1MjMxODM0MTdaMIGUMQswCQYD
                VQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsG
                A1UECgwET2t0YTEUMBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGRldi0xNjk5NDUxNzEc
                MBoGCSqGSIb3DQEJARYNaW5mb0Bva3RhLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
                ggEBANMQI4i1roai7bnDCAiwDr3FbkKz6RkTOi1Uz1qjnIRfyWIHJRa2yUmjN3+wBmTBHYNkxgMK
                I3g8iElMX3Fz/FFjEYKsCNAq4RZG+sn/zo/8Y6g7bMvz7kc/oXikiuSK/BWFkvx7rSm1fRA+cX6W
                iy3HlsqNPXLUMXlZYV5RK8vF0wxITVJxyvxBaQeKezJD+CNIxVwMBZfgptMxIbKMEHcucVqkp8sa
                aQt0/9Xjser0DbMwPVHKctCyjkXUz/rMfWIw7E6ehL3gFKfHfZn/Mld8PzFg71Ql7AqkYZ8gB9HO
                xUXEeqvIMlqsMu3IlVsEAhF4m+S75TJQJdpvW8NiiRUCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEA
                iOoPf0SRBZE3aE4O65HCYwmCNRBJdbCJqqBEcT1rHUuACCtyq4KB1sOPZfoHURHern7o8jB3UpCV
                aVgdYX05FIkfZnGHYxeZ/7exeDW0kVydhpVouqCqSAdyDhci053Isz2VwAvs5zh2oTa5ChFFZ4bS
                WSmv/eM6RhBePRYe+pExiFhMy2+Rx8O4UV1hTQMr2s3Zp6YYUMqPC23t/3wQaY5YskbZ4E3Qsq6K
                iB7h/2MLj4XZnX+cdmdYmS8K1fPsBPiz5B35v3CqvpzcmfVVyPlIzDVWe87AJneAcqxRrnhHFO3N
                20Qc7OFBZxC0xde8mrIfIaX4y99g4yk8hzHqRQ==
                -----END CERTIFICATE-----"""
}

DEFAULT_ORGS = ["datadotworldsupport", "ddw", "datadotworld-apps"]


def create_site(admin_token, entity_id, public_slug, sso_url, x509_cert, api_url):
    url = f"{api_url}/admin/sites/create"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    # Prepare the data to be sent in the request
    data = {
        'entityid': entity_id,
        'publicSlug': public_slug,
        'ssoUrl': sso_url,
        'x509Certificate': x509_cert
    }

    body = json.dumps(data)
    response = requests.post(url, body, cookies=cookies, headers=header)

    if response.status_code == 200:
        print(f"Successfully created the site: {response.text}")
    else:
        print(response.text)


def edit_saml(admin_token, entity_id, site_id, default_org_list, sso_url, x509_cert, api_url):
    resource_id = f"site%3A{site_id}"
    url = f"{api_url}/admin/saml/{resource_id}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    # Prepare the data to be sent in the request
    data = {
      "agentid": site_id,
      "defaultOrgList": default_org_list,
      "entityid": entity_id,
      "ssoUrl": sso_url,
      "x509Certificate": x509_cert
    }

    body = json.dumps(data)
    response = requests.put(url, body, cookies=cookies, headers=header)

    if response.status_code == 200:
        print(f"Successfully updated SAML!")
        print(f"Entity ID: {entity_id}")
        print(f"SSO Url: {sso_url}")
        print(f"x509 Certificate: {x509_cert}")
    else:
        print(response.text)


def get_site_id(admin_token, public_slug, api_url):
    url = f"{api_url}/site/slug/{public_slug}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    response = requests.get(url, cookies=cookies, headers=header)

    if response.status_code == 200:
        response_json = response.json()
        site_id = response_json['site']
        print(f"Found site_id: {site_id} for {public_slug}")

        return site_id, True
    else:
        print(response.text)
        return None, False
