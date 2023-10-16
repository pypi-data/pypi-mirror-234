## Modulos Client Tool

This tool provides a command-line interface to interact with the Modulos platform. 

### Prerequisites

- Python 3.x
- Setuptools and wheels:
```
pip install --upgrade pip setuptools wheel
```
- Install dependencies: 

```
pip install modulos-client
```

### Usage

#### Logging In

To login to the Modulos platform:

```bash
modulos login --host [HOST_URL] --token [TOKEN] --profile-name [PROFILE_NAME]
```

- `[HOST]` is the address of the platform. For local use, this would typically be `http://localhost`.
- `[TOKEN]` is your authentication token.
- `[PROFILE_NAME]` is the name of the profile. It is used to reference the profile in the future. If you want to use multiple profiles, you can specify a different name for each profile.

#### Logging Out

To logout from the Modulos platform:

```bash
modulos logout
```

#### List profiles

List all profiles:

```bash
modulos profile list
```

#### Profile activation

Activate a profile:

```bash
modulos profiles activate --profile-name [PROFILE_NAME]
```

#### Managing Organizations

List all organizations:

```bash
modulos orgs list
```

Create a new organization:

```bash
modulos orgs create --name [ORG_NAME]
```

Delete an organization:

```bash
modulos orgs delete --name [ORG_NAME]
```

#### Managing Users

List all users:

```bash
modulos users list
```

Create a new user:

```bash
modulos users create --organization [ORG_NAME] --firstname [FIRST_NAME] --lastname [LAST_NAME] --email [EMAIL] --azure-oid [AZURE_OID] --is-active [IS_ACTIVE]
```

#### Managing Projects

List all projects:

```bash
modulos projects list --page [PAGE_NUMBER]
```

Delete a project:

```bash
modulos projects delete --id [PROJECT_ID]
```

#### Managing Templates

List all templates:

```bash
modulos templates list
```

Upload templates for your organization:

```bash
modulos templates upload --file [FILE_PATH]
```

---

For a detailed list of available commands and their options, run:

```bash
modulos --help
```

This will provide a comprehensive list of commands and their descriptions.

---

© 2023 Modulos AG. All rights reserved.
