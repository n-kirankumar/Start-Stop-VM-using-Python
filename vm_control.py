import argparse
import logging
from google.cloud import compute_v1
from google.api_core.exceptions import NotFound, Forbidden

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
def get_vm_status(project, zone, vm_name):
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
def start_vm(project, zone, vm_name):
    client = compute_v1.InstancesClient()
    logging.info(f"Starting VM: {vm_name}")
    client.start(
        project=project,
        zone=zone,
        instance=vm_name
    )

def stop_vm(project, zone, vm_name):
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
def main():
    parser = argparse.ArgumentParser(description="Production-grade GCP VM lifecycle automation")
    parser.add_argument("--action", choices=["start", "stop"], required=True)

    args = parser.parse_args()

    PROJECT_ID = "eng-archery-480704-i7"
    ZONE = "asia-south1-a"
    VM_NAME = "dev-backend-vm"

    try:
        status = get_vm_status(PROJECT_ID, ZONE, VM_NAME)
        logging.info(f"Current VM status: {status}")

        if args.action == "stop":
            if status == "TERMINATED":
                logging.warning("VM already stopped. No action needed.")
                return
            stop_vm(PROJECT_ID, ZONE, VM_NAME)
            logging.info("Stop request sent successfully")

        if args.action == "start":
            if status == "RUNNING":
                logging.warning("VM already running. No action needed.")
                return
            start_vm(PROJECT_ID, ZONE, VM_NAME)
            logging.info("Start request sent successfully")

    except NotFound:
        logging.error("VM not found. Check project, zone, or VM name.")
    except Forbidden:
        logging.error("Permission denied. Check IAM roles.")
    except Exception as e:
        logging.exception(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

