#define _GNU_SOURCE
#include <arpa/inet.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

static char PROJECT_DIR[PATH_MAX] = ".";

static void init_project_dir(const char *argv0) {
    char resolved[PATH_MAX];

    if (realpath(argv0, resolved) == NULL) {
        if (getcwd(PROJECT_DIR, sizeof(PROJECT_DIR)) == NULL) {
            strncpy(PROJECT_DIR, ".", sizeof(PROJECT_DIR) - 1);
        }
        return;
    }

    char *last = strrchr(resolved, '/');
    if (last) *last = '\0';

    char *last_dir = strrchr(resolved, '/');
    if (last_dir && strcmp(last_dir + 1, "bin") == 0) {
        *last_dir = '\0';
    }

    strncpy(PROJECT_DIR, resolved, sizeof(PROJECT_DIR) - 1);
    PROJECT_DIR[sizeof(PROJECT_DIR) - 1] = '\0';
}

static void write_log(const char *fmt, ...) {
    char path[PATH_MAX];
    snprintf(path, sizeof(path), "%s/logs/linux_manager.log", PROJECT_DIR);

    FILE *f = fopen(path, "a");
    if (!f) return;

    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    char tbuf[64];
    strftime(tbuf, sizeof(tbuf), "%Y-%m-%d %H:%M:%S", tm_info);

    fprintf(f, "%s - ", tbuf);

    va_list args;
    va_start(args, fmt);
    vfprintf(f, fmt, args);
    va_end(args);

    fprintf(f, "\n");
    fclose(f);
}

static int run_cmd(const char *cmd) {
    int status = system(cmd);
    if (status == -1) {
        printf("Không thể chạy lệnh: %s\n", strerror(errno));
        return 1;
    }
    if (WIFEXITED(status)) return WEXITSTATUS(status);
    return 1;
}

static void shell_quote(const char *input, char *output, size_t size) {
    size_t j = 0;

    if (size == 0) return;
    output[j++] = '\'';

    for (size_t i = 0; input[i] != '\0' && j < size - 1; i++) {
        if (input[i] == '\'') {
            const char *seq = "'\\''";
            for (size_t k = 0; seq[k] != '\0' && j < size - 1; k++) {
                output[j++] = seq[k];
            }
        } else {
            output[j++] = input[i];
        }
    }

    if (j < size - 1) output[j++] = '\'';
    output[j] = '\0';
}

static int exists_path(const char *path) {
    struct stat st;
    return stat(path, &st) == 0;
}

static int is_dir(const char *path) {
    struct stat st;
    return stat(path, &st) == 0 && S_ISDIR(st.st_mode);
}

static int is_file(const char *path) {
    struct stat st;
    return stat(path, &st) == 0 && S_ISREG(st.st_mode);
}

static void print_usage(void) {
    printf("LINUX SYSTEM MANAGER C BACKEND\n");
    printf("\n");
    printf("PROCESS:\n");
    printf("  linux_manager process list\n");
    printf("  linux_manager process search <keyword>\n");
    printf("  linux_manager process detail <pid>\n");
    printf("  linux_manager process kill <pid>\n");
    printf("  linux_manager process top\n");
    printf("\n");
    printf("FILE:\n");
    printf("  linux_manager file list <dir>\n");
    printf("  linux_manager file info <path>\n");
    printf("  linux_manager file create-file <path>\n");
    printf("  linux_manager file create-dir <path>\n");
    printf("  linux_manager file copy <src> <dst>\n");
    printf("  linux_manager file move <src> <dst>\n");
    printf("  linux_manager file delete <path>\n");
    printf("  linux_manager file view <file>\n");
    printf("\n");
    printf("SOCKET:\n");
    printf("  linux_manager socket server <port>\n");
    printf("  linux_manager socket client <host> <port> <message>\n");
    printf("\n");
    printf("NETWORK:\n");
    printf("  linux_manager network interfaces\n");
    printf("  linux_manager network routes\n");
    printf("  linux_manager network ping <host>\n");
    printf("  linux_manager network dns <host>\n");
    printf("  linux_manager network ports\n");
}

static int process_list(void) {
    write_log("Xem danh sách tiến trình");
    return run_cmd("ps -eo pid,ppid,user,stat,%cpu,%mem,comm --sort=pid | head -n 80");
}

static int process_search(const char *keyword) {
    char qkeyword[PATH_MAX * 2];
    char cmd[PATH_MAX * 3];

    shell_quote(keyword, qkeyword, sizeof(qkeyword));
    snprintf(cmd, sizeof(cmd), "ps aux | grep -i -- %s | grep -v grep", qkeyword);

    write_log("Tìm tiến trình theo từ khóa: %s", keyword);
    return run_cmd(cmd);
}

static int process_detail(const char *pid) {
    char qpid[128];
    char cmd[512];

    shell_quote(pid, qpid, sizeof(qpid));
    snprintf(cmd, sizeof(cmd), "ps -p %s -o pid,ppid,user,stat,etime,%%cpu,%%mem,cmd", qpid);

    write_log("Xem chi tiết tiến trình PID=%s", pid);
    return run_cmd(cmd);
}

static int process_kill(const char *pid_str) {
    char *end = NULL;
    long pid = strtol(pid_str, &end, 10);

    if (end == pid_str || *end != '\0' || pid <= 1) {
        printf("PID không hợp lệ hoặc không được phép kill PID <= 1.\n");
        return 1;
    }

    if (kill((pid_t)pid, SIGTERM) == 0) {
        printf("Đã gửi SIGTERM tới tiến trình PID %ld.\n", pid);
        write_log("Kill tiến trình PID=%ld", pid);
        return 0;
    }

    printf("Kill thất bại: %s\n", strerror(errno));
    return 1;
}

static int process_top(void) {
    write_log("Xem tiến trình dùng CPU cao");
    return run_cmd("ps -eo pid,ppid,user,%cpu,%mem,comm --sort=-%cpu | head -n 20");
}

static int file_list(const char *dir) {
    if (!is_dir(dir)) {
        printf("Thư mục không tồn tại.\n");
        return 1;
    }

    char qdir[PATH_MAX * 2];
    char cmd[PATH_MAX * 3];

    shell_quote(dir, qdir, sizeof(qdir));
    snprintf(cmd, sizeof(cmd), "ls -lah %s", qdir);

    write_log("Xem danh sách file/thư mục: %s", dir);
    return run_cmd(cmd);
}

static int file_info(const char *path) {
    if (!exists_path(path)) {
        printf("Đường dẫn không tồn tại.\n");
        return 1;
    }

    char qpath[PATH_MAX * 2];
    char cmd[PATH_MAX * 3];

    shell_quote(path, qpath, sizeof(qpath));
    snprintf(cmd, sizeof(cmd), "stat %s", qpath);

    write_log("Xem thông tin file/thư mục: %s", path);
    return run_cmd(cmd);
}

static int file_create_file(const char *path) {
    if (exists_path(path)) {
        printf("File/thư mục đã tồn tại.\n");
        return 1;
    }

    FILE *f = fopen(path, "w");
    if (!f) {
        printf("Tạo file thất bại: %s\n", strerror(errno));
        return 1;
    }

    fclose(f);
    printf("Đã tạo file: %s\n", path);
    write_log("Tạo file: %s", path);
    return 0;
}

static int file_create_dir(const char *path) {
    char qpath[PATH_MAX * 2];
    char cmd[PATH_MAX * 3];

    shell_quote(path, qpath, sizeof(qpath));
    snprintf(cmd, sizeof(cmd), "mkdir -p %s", qpath);

    int rc = run_cmd(cmd);
    if (rc == 0) {
        printf("Đã tạo thư mục: %s\n", path);
        write_log("Tạo thư mục: %s", path);
    }
    return rc;
}

static int file_copy(const char *src, const char *dst) {
    if (!exists_path(src)) {
        printf("Nguồn không tồn tại.\n");
        return 1;
    }

    char qsrc[PATH_MAX * 2], qdst[PATH_MAX * 2];
    char cmd[PATH_MAX * 5];

    shell_quote(src, qsrc, sizeof(qsrc));
    shell_quote(dst, qdst, sizeof(qdst));
    snprintf(cmd, sizeof(cmd), "cp -r %s %s", qsrc, qdst);

    int rc = run_cmd(cmd);
    if (rc == 0) {
        printf("Đã sao chép thành công.\n");
        write_log("Sao chép từ %s đến %s", src, dst);
    }
    return rc;
}

static int file_move(const char *src, const char *dst) {
    if (!exists_path(src)) {
        printf("Nguồn không tồn tại.\n");
        return 1;
    }

    char qsrc[PATH_MAX * 2], qdst[PATH_MAX * 2];
    char cmd[PATH_MAX * 5];

    shell_quote(src, qsrc, sizeof(qsrc));
    shell_quote(dst, qdst, sizeof(qdst));
    snprintf(cmd, sizeof(cmd), "mv %s %s", qsrc, qdst);

    int rc = run_cmd(cmd);
    if (rc == 0) {
        printf("Đã di chuyển/đổi tên thành công.\n");
        write_log("Di chuyển/đổi tên từ %s đến %s", src, dst);
    }
    return rc;
}

static int file_delete(const char *path) {
    if (!exists_path(path)) {
        printf("Đường dẫn không tồn tại.\n");
        return 1;
    }

    char qpath[PATH_MAX * 2];
    char cmd[PATH_MAX * 3];

    shell_quote(path, qpath, sizeof(qpath));
    snprintf(cmd, sizeof(cmd), "rm -r %s", qpath);

    int rc = run_cmd(cmd);
    if (rc == 0) {
        printf("Đã xóa thành công.\n");
        write_log("Xóa file/thư mục: %s", path);
    }
    return rc;
}

static int file_view(const char *path) {
    if (!is_file(path)) {
        printf("File không tồn tại hoặc không phải file thường.\n");
        return 1;
    }

    FILE *f = fopen(path, "r");
    if (!f) {
        printf("Không thể mở file: %s\n", strerror(errno));
        return 1;
    }

    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), f)) {
        fputs(buffer, stdout);
    }

    fclose(f);
    write_log("Xem nội dung file: %s", path);
    return 0;
}

static int socket_server(const char *port_str) {
    int port = atoi(port_str);
    if (port <= 0 || port > 65535) {
        printf("Port không hợp lệ.\n");
        return 1;
    }

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        printf("Tạo socket thất bại: %s\n", strerror(errno));
        return 1;
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons((uint16_t)port);

    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        printf("Bind thất bại: %s\n", strerror(errno));
        close(server_fd);
        return 1;
    }

    if (listen(server_fd, 5) < 0) {
        printf("Listen thất bại: %s\n", strerror(errno));
        close(server_fd);
        return 1;
    }

    printf("Echo server đang chạy tại port %d...\n", port);
    fflush(stdout);
    write_log("Khởi động echo server port %d", port);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);

        if (client_fd < 0) {
            continue;
        }

        char buffer[1024];
        ssize_t n = recv(client_fd, buffer, sizeof(buffer) - 1, 0);

        if (n > 0) {
            buffer[n] = '\0';
            char reply[1200];
            snprintf(reply, sizeof(reply), "Server received: %s", buffer);
            send(client_fd, reply, strlen(reply), 0);
        }

        close(client_fd);
    }

    close(server_fd);
    return 0;
}

static int socket_client(const char *host, const char *port_str, const char *message) {
    int port = atoi(port_str);
    if (port <= 0 || port > 65535) {
        printf("Port không hợp lệ.\n");
        return 1;
    }

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        printf("Tạo socket client thất bại: %s\n", strerror(errno));
        return 1;
    }

    struct hostent *server = gethostbyname(host);
    if (!server) {
        printf("Không tìm thấy host: %s\n", host);
        close(sockfd);
        return 1;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    memcpy(&server_addr.sin_addr.s_addr, server->h_addr, (size_t)server->h_length);
    server_addr.sin_port = htons((uint16_t)port);

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("Kết nối thất bại: %s\n", strerror(errno));
        close(sockfd);
        return 1;
    }

    send(sockfd, message, strlen(message), 0);

    char buffer[2048];
    ssize_t n = recv(sockfd, buffer, sizeof(buffer) - 1, 0);
    if (n > 0) {
        buffer[n] = '\0';
        printf("%s\n", buffer);
    }

    close(sockfd);
    write_log("Socket client gửi tới %s:%d", host, port);
    return 0;
}

static int network_interfaces(void) {
    write_log("Xem thông tin interface mạng");
    return run_cmd("ip addr");
}

static int network_routes(void) {
    write_log("Xem bảng định tuyến");
    return run_cmd("ip route");
}

static int network_ping(const char *host) {
    char qhost[PATH_MAX * 2];
    char cmd[PATH_MAX * 3];

    shell_quote(host, qhost, sizeof(qhost));
    snprintf(cmd, sizeof(cmd), "ping -c 4 %s", qhost);

    write_log("Ping host: %s", host);
    return run_cmd(cmd);
}

static int network_dns(const char *host) {
    struct addrinfo hints, *res, *p;
    char ipstr[INET6_ADDRSTRLEN];

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;

    int status = getaddrinfo(host, NULL, &hints, &res);
    if (status != 0) {
        printf("DNS lookup thất bại: %s\n", gai_strerror(status));
        return 1;
    }

    printf("Kết quả phân giải DNS cho %s:\n", host);

    for (p = res; p != NULL; p = p->ai_next) {
        void *addr;

        if (p->ai_family == AF_INET) {
            struct sockaddr_in *ipv4 = (struct sockaddr_in *)p->ai_addr;
            addr = &(ipv4->sin_addr);
        } else if (p->ai_family == AF_INET6) {
            struct sockaddr_in6 *ipv6 = (struct sockaddr_in6 *)p->ai_addr;
            addr = &(ipv6->sin6_addr);
        } else {
            continue;
        }

        inet_ntop(p->ai_family, addr, ipstr, sizeof(ipstr));
        printf("%s\n", ipstr);
    }

    freeaddrinfo(res);
    write_log("DNS lookup: %s", host);
    return 0;
}

static int network_ports(void) {
    write_log("Xem port đang lắng nghe");
    return run_cmd("ss -tuln");
}

int main(int argc, char *argv[]) {
    init_project_dir(argv[0]);

    if (argc < 2) {
        print_usage();
        return 1;
    }

    if (strcmp(argv[1], "process") == 0) {
        if (argc < 3) {
            print_usage();
            return 1;
        }

        if (strcmp(argv[2], "list") == 0) return process_list();
        if (strcmp(argv[2], "search") == 0 && argc >= 4) return process_search(argv[3]);
        if (strcmp(argv[2], "detail") == 0 && argc >= 4) return process_detail(argv[3]);
        if (strcmp(argv[2], "kill") == 0 && argc >= 4) return process_kill(argv[3]);
        if (strcmp(argv[2], "top") == 0) return process_top();

        print_usage();
        return 1;
    }

    if (strcmp(argv[1], "file") == 0) {
        if (argc < 3) {
            print_usage();
            return 1;
        }

        if (strcmp(argv[2], "list") == 0 && argc >= 4) return file_list(argv[3]);
        if (strcmp(argv[2], "info") == 0 && argc >= 4) return file_info(argv[3]);
        if (strcmp(argv[2], "create-file") == 0 && argc >= 4) return file_create_file(argv[3]);
        if (strcmp(argv[2], "create-dir") == 0 && argc >= 4) return file_create_dir(argv[3]);
        if (strcmp(argv[2], "copy") == 0 && argc >= 5) return file_copy(argv[3], argv[4]);
        if (strcmp(argv[2], "move") == 0 && argc >= 5) return file_move(argv[3], argv[4]);
        if (strcmp(argv[2], "delete") == 0 && argc >= 4) return file_delete(argv[3]);
        if (strcmp(argv[2], "view") == 0 && argc >= 4) return file_view(argv[3]);

        print_usage();
        return 1;
    }

    if (strcmp(argv[1], "socket") == 0) {
        if (argc < 3) {
            print_usage();
            return 1;
        }

        if (strcmp(argv[2], "server") == 0 && argc >= 4) return socket_server(argv[3]);
        if (strcmp(argv[2], "client") == 0 && argc >= 6) return socket_client(argv[3], argv[4], argv[5]);

        print_usage();
        return 1;
    }

    if (strcmp(argv[1], "network") == 0) {
        if (argc < 3) {
            print_usage();
            return 1;
        }

        if (strcmp(argv[2], "interfaces") == 0) return network_interfaces();
        if (strcmp(argv[2], "routes") == 0) return network_routes();
        if (strcmp(argv[2], "ping") == 0 && argc >= 4) return network_ping(argv[3]);
        if (strcmp(argv[2], "dns") == 0 && argc >= 4) return network_dns(argv[3]);
        if (strcmp(argv[2], "ports") == 0) return network_ports();

        print_usage();
        return 1;
    }

    print_usage();
    return 1;
}
