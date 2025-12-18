Notion Link
https://www.notion.so/GCP-VM-Start-Stop-Automation-2cd23cb201b580f3af6ec53c7dce3624?source=copy_link


We will use **your real configuration**:

```
PROJECT ID : eng-archery-480704-i7
ZONE       : asia-south1-a
VM NAME    : dev-backend-vm

```

---

## 1️⃣ Preconditions (Verify Once)

### ✅ GCP CLI Auth (already done, but verify)

```bash
gcloud auth list

```

Expected:

```
* gcpg0310@gmail.com

```

### ✅ ADC (Application Default Credentials)

```bash
gcloud auth application-default login

```

(Required for Python → GCP API)

---

## 2️⃣ Create Project Workspace (FROM SCRATCH)

```bash
mkdir gcp-vm-automation
cd gcp-vm-automation

```

---

## 3️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

```

Verify:

```bash
which python

```

Should point to `gcp-vm-automation/venv`

---

## 4️⃣ Create `requirements.txt`

```bash
cat <<EOF > requirements.txt
google-cloud-compute
google-auth
EOF

```

Install:

```bash
pip install -r requirements.txt

```

---

## 5️⃣ Create Production-Ready Python Script

### 📄 `vm_control.py`

```bash
nano vm_control.py

```

Paste **exactly** this:

```python
import argparse
import logging
from google.cloudimport compute_v1
from google.api_core.exceptionsimport NotFound, Forbidden

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------
# VM Status Fetch
# -------------------------
defget_vm_status(project, zone, vm_name):
    client = compute_v1.InstancesClient()
    instance = client.get(
        project=project,
        zone=zone,
        instance=vm_name
    )
return instance.status

# -------------------------
# VM Operations
# -------------------------
defstart_vm(project, zone, vm_name):
    client = compute_v1.InstancesClient()
    logging.info(f"Starting VM: {vm_name}")
    client.start(
        project=project,
        zone=zone,
        instance=vm_name
    )

defstop_vm(project, zone, vm_name):
    client = compute_v1.InstancesClient()
    logging.info(f"Stopping VM: {vm_name}")
    client.stop(
        project=project,
        zone=zone,
        instance=vm_name
    )

# -------------------------
# Main
# -------------------------
defmain():
    parser = argparse.ArgumentParser(description="Production-grade GCP VM lifecycle automation")
    parser.add_argument("--action", choices=["start","stop"], required=True)

    args = parser.parse_args()

    PROJECT_ID ="eng-archery-480704-i7"
    ZONE ="asia-south1-a"
    VM_NAME ="dev-backend-vm"

try:
        status = get_vm_status(PROJECT_ID, ZONE, VM_NAME)
        logging.info(f"Current VM status: {status}")

if args.action =="stop":
if status =="TERMINATED":
                logging.warning("VM already stopped. No action needed.")
return
            stop_vm(PROJECT_ID, ZONE, VM_NAME)
            logging.info("Stop request sent successfully")

if args.action =="start":
if status =="RUNNING":
                logging.warning("VM already running. No action needed.")
return
            start_vm(PROJECT_ID, ZONE, VM_NAME)
            logging.info("Start request sent successfully")

except NotFound:
        logging.error("VM not found. Check project, zone, or VM name.")
except Forbidden:
        logging.error("Permission denied. Check IAM roles.")
except Exceptionas e:
        logging.exception(f"Unexpected error occurred: {e}")

if __name__ =="__main__":
    main()

```

Save and exit.

---

## 6️⃣ RUN — STOP THE VM (REAL ACTION)

```bash
python vm_control.py --action stop

```

### ✅ Expected Output

```
INFO | Current VM status: RUNNING
INFO | Stopping VM: dev-backend-vm
INFO | Stop request sent successfully

```

### ✅ Verify in GCP Console

VM status → **TERMINATED**

---

## 7️⃣ RUN — START THE VM

```bash
python vm_control.py --action start

```

### ✅ Expected Output

```
INFO | Current VM status: TERMINATED
INFO | Starting VM: dev-backend-vm
INFO | Start request sent successfully

```

---

## 8️⃣ WHY THIS IS **PRODUCTION-READY** (Interview Gold)

| Feature | Implemented |
| --- | --- |
| No IP hardcoding | ✅ |
| IAM-based auth | ✅ |
| Status validation | ✅ |
| Idempotent logic | ✅ |
| Exception handling | ✅ |
| Structured logging | ✅ |
| Safe cloud operations | ✅ |

---

## 🎯 Interview Explanation (Say This)

> “We automated Compute Engine VM lifecycle management using Python and GCP SDKs with IAM-based authentication, status validation, and proper exception handling to safely reduce cloud costs.”
> 

---

## 🧾 Resume Line (Use As-Is)

> Automated GCP VM start/stop operations using Python and Google Cloud APIs with production-grade error handling and logging to optimize infrastructure costs.
> 

Automated GCP VM start/stop operations using Python and Google Cloud APIs with production-grade error handling and logging to optimize infrastructure costs.

![image.png](attachment:3f013682-95de-4358-ad80-db2f441fafce:image.png)

![image.png](attachment:477b44d5-411b-4aac-ac62-f73c12245aff:image.png)

![image.png](attachment:39452543-4050-431b-b42f-16d1c911ce0f:image.png)

![image.png](attachment:6bbcb03a-c94c-4b0a-bf62-99281f4bcfed:image.png)
