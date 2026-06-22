#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/version.h>

#define ROWS 3
#define COLS 3
#define PROC_NAME "matrix_module"

static int matrix1[ROWS][COLS] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

static int matrix2[ROWS][COLS] = {
    {10, 4, 7},
    {6, 9, 4},
    {3, 7, 1}
};

static struct proc_dir_entry *proc_entry;

static int max_matrix(int matrix[ROWS][COLS])
{
    int max_value = matrix[0][0];
    int i, j;

    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            if (matrix[i][j] > max_value) {
                max_value = matrix[i][j];
            }
        }
    }

    return max_value;
}

static int min_matrix(int matrix[ROWS][COLS])
{
    int min_value = matrix[0][0];
    int i, j;

    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            if (matrix[i][j] < min_value) {
                min_value = matrix[i][j];
            }
        }
    }

    return min_value;
}

static int is_prime(int n)
{
    int i;

    if (n < 2) {
        return 0;
    }

    for (i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            return 0;
        }
    }

    return 1;
}

static int count_primes(int matrix[ROWS][COLS])
{
    int count = 0;
    int i, j;

    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            if (is_prime(matrix[i][j])) {
                count++;
            }
        }
    }

    return count;
}

static void add_matrices(int result[ROWS][COLS])
{
    int i, j;

    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            result[i][j] = matrix1[i][j] + matrix2[i][j];
        }
    }
}

static void multiply_matrices(int result[ROWS][COLS])
{
    int i, j, k;

    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            result[i][j] = 0;
            for (k = 0; k < COLS; k++) {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

static void print_matrix_to_log(const char *name, int matrix[ROWS][COLS])
{
    int i;

    printk(KERN_INFO "%s:\n", name);
    for (i = 0; i < ROWS; i++) {
        printk(KERN_INFO "%d\t%d\t%d\n",
               matrix[i][0], matrix[i][1], matrix[i][2]);
    }
}

static void seq_print_matrix(struct seq_file *m, const char *name, int matrix[ROWS][COLS])
{
    int i, j;

    seq_printf(m, "%s:\n", name);
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            seq_printf(m, "%d\t", matrix[i][j]);
        }
        seq_puts(m, "\n");
    }
}

static int matrix_proc_show(struct seq_file *m, void *v)
{
    int sum[ROWS][COLS];
    int product[ROWS][COLS];

    add_matrices(sum);
    multiply_matrices(product);

    seq_puts(m, "===== MATRIX KERNEL MODULE =====\n\n");

    seq_print_matrix(m, "Matrix 1", matrix1);
    seq_puts(m, "\n");

    seq_print_matrix(m, "Matrix 2", matrix2);
    seq_puts(m, "\n");

    seq_printf(m, "Max matrix 1: %d\n", max_matrix(matrix1));
    seq_printf(m, "Min matrix 1: %d\n", min_matrix(matrix1));
    seq_printf(m, "Prime count matrix 1: %d\n\n", count_primes(matrix1));

    seq_printf(m, "Max matrix 2: %d\n", max_matrix(matrix2));
    seq_printf(m, "Min matrix 2: %d\n", min_matrix(matrix2));
    seq_printf(m, "Prime count matrix 2: %d\n\n", count_primes(matrix2));

    seq_print_matrix(m, "Matrix 1 + Matrix 2", sum);
    seq_puts(m, "\n");

    seq_print_matrix(m, "Matrix 1 * Matrix 2", product);

    return 0;
}

static int matrix_proc_open(struct inode *inode, struct file *file)
{
    return single_open(file, matrix_proc_show, NULL);
}

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
static const struct proc_ops matrix_proc_ops = {
    .proc_open = matrix_proc_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};
#else
static const struct file_operations matrix_proc_ops = {
    .owner = THIS_MODULE,
    .open = matrix_proc_open,
    .read = seq_read,
    .llseek = seq_lseek,
    .release = single_release,
};
#endif

static int __init matrix_module_init(void)
{
    int sum[ROWS][COLS];
    int product[ROWS][COLS];

    printk(KERN_INFO "Matrix kernel module: loading...\n");

    proc_entry = proc_create(PROC_NAME, 0444, NULL, &matrix_proc_ops);
    if (!proc_entry) {
        printk(KERN_ERR "Matrix kernel module: cannot create /proc/%s\n", PROC_NAME);
        return -ENOMEM;
    }

    add_matrices(sum);
    multiply_matrices(product);

    print_matrix_to_log("Matrix 1", matrix1);
    print_matrix_to_log("Matrix 2", matrix2);

    printk(KERN_INFO "Max matrix 1 = %d\n", max_matrix(matrix1));
    printk(KERN_INFO "Min matrix 1 = %d\n", min_matrix(matrix1));
    printk(KERN_INFO "Prime count matrix 1 = %d\n", count_primes(matrix1));

    printk(KERN_INFO "Max matrix 2 = %d\n", max_matrix(matrix2));
    printk(KERN_INFO "Min matrix 2 = %d\n", min_matrix(matrix2));
    printk(KERN_INFO "Prime count matrix 2 = %d\n", count_primes(matrix2));

    print_matrix_to_log("Matrix 1 + Matrix 2", sum);
    print_matrix_to_log("Matrix 1 * Matrix 2", product);

    printk(KERN_INFO "Matrix kernel module: loaded. Read /proc/%s\n", PROC_NAME);
    return 0;
}

static void __exit matrix_module_exit(void)
{
    remove_proc_entry(PROC_NAME, NULL);
    printk(KERN_INFO "Matrix kernel module: unloaded.\n");
}

module_init(matrix_module_init);
module_exit(matrix_module_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Thinh");
MODULE_DESCRIPTION("Simple Linux kernel module integrated with /proc to process matrices");
MODULE_VERSION("1.0");
