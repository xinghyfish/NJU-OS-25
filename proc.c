#include <stdio.h>
#include <stdlib.h>
#include <sys/sysctl.h>
#include <libproc.h>
#include <mach/mach_time.h>
#include <unistd.h>

void print_process_info(pid_t pid) {
    // 获取进程的基本信息
    struct proc_bsdinfo proc;
    int ret = proc_pidinfo(pid, PROC_PIDTBSDINFO, 0, &proc, sizeof(proc));
    if (ret <= 0) {
        perror("proc_pidinfo (PROC_PIDTBSDINFO)");
        return;
    }

    printf("PID: %d\n", proc.pbi_pid);
    printf("Process Name: %s\n", proc.pbi_name);
    printf("Parent PID: %d\n", proc.pbi_ppid);
    printf("User ID: %d\n", proc.pbi_uid);
    printf("Group ID: %d\n", proc.pbi_gid);
    printf("Status: %c\n", proc.pbi_status);

    // 获取进程的内存使用情况
    struct proc_taskinfo task_info;
    ret = proc_pidinfo(pid, PROC_PIDTASKINFO, 0, &task_info, sizeof(task_info));
    if (ret <= 0) {
        perror("proc_pidinfo (PROC_PIDTASKINFO)");
        return;
    }

    printf("Resident Memory: %llu MB\n", task_info.pti_resident_size >> 20);
    printf("Virtual Memory: %llu GB\n", task_info.pti_virtual_size >> 30);

    // 计算 CPU 时间（用户态 + 内核态）
    uint64_t total_time = task_info.pti_total_user + task_info.pti_total_system;
    printf("Total CPU Time: %llu nanoseconds\n", total_time);
}

int main(int argc, char *argv[]) {
    if (argc != 1) {
        fprintf(stderr, "Usage: %s <pid>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    pid_t pid = getpid();
    print_process_info(pid);

    return 0;
}