from typing import Any, Dict, List

from prefect.infrastructure.kubernetes import KubernetesJob

# review package name


def create_infrastructure(
    docker_image: str,
    kedro_package: str,
    image_pull_policy: str = "Always",
    finished_job_ttl: int = 43200,
    pod_watch_timeout_seconds: int = 360,
    container_memory: str = "3Gi",
    container_cpu: str = "1",
    container_storage: str = "4096Mi",
    job_template: Dict[str, Any] = None,
    customizations: List[Dict[str, Any]] = None,
    job_name: str = None,
    command: List[str] = None,
):
    extra_loggers = kedro_package.replace("-", "_").replace(" ", "_")
    customizations = customizations if customizations else []
    customizations.append(
        {
            "op": "add",
            "path": "/spec/template/spec/containers/0/resources",
            "value": {
                "requests": {
                    "cpu": container_cpu,
                    "memory": container_memory,
                    "ephemeral-storage": container_storage,
                }
            },
        }
    )
    kubernetes_job = KubernetesJob(
        image=docker_image,
        image_pull_policy=image_pull_policy,
        finished_job_ttl=finished_job_ttl,
        pod_watch_timeout_seconds=pod_watch_timeout_seconds,
        namespace="prefect2",
        env={
            "PREFECT_LOGGING_EXTRA_LOGGERS": f"kedro,{extra_loggers}",
        },
        job=job_template if job_template else KubernetesJob.base_job_manifest(),
        customizations=customizations,
        command=command,
    )

    if not job_name:
        job_name = f"{kedro_package.replace('_', '-')}-kubernetes-job"
    kubernetes_job.save(job_name, overwrite=True)


if __name__ == "__main__":
    create_infrastructure()
