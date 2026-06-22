#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x2c7db5ac, "remove_proc_entry" },
	{ 0xd7fc4fd0, "seq_write" },
	{ 0x2be27a2d, "seq_read" },
	{ 0x2885ab8e, "seq_lseek" },
	{ 0x3cdc139e, "single_release" },
	{ 0xd272d446, "__fentry__" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0x90a48d82, "__ubsan_handle_out_of_bounds" },
	{ 0xe8213e80, "_printk" },
	{ 0xbd03ed67, "__ref_stack_chk_guard" },
	{ 0x1c77f2cc, "proc_create" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0x5ed2ae1d, "single_open" },
	{ 0x48b2cb88, "seq_printf" },
	{ 0xc9a058b9, "seq_putc" },
	{ 0xa3ed642b, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0x2c7db5ac,
	0xd7fc4fd0,
	0x2be27a2d,
	0x2885ab8e,
	0x3cdc139e,
	0xd272d446,
	0xd272d446,
	0x90a48d82,
	0xe8213e80,
	0xbd03ed67,
	0x1c77f2cc,
	0xd272d446,
	0x5ed2ae1d,
	0x48b2cb88,
	0xc9a058b9,
	0xa3ed642b,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"remove_proc_entry\0"
	"seq_write\0"
	"seq_read\0"
	"seq_lseek\0"
	"single_release\0"
	"__fentry__\0"
	"__x86_return_thunk\0"
	"__ubsan_handle_out_of_bounds\0"
	"_printk\0"
	"__ref_stack_chk_guard\0"
	"proc_create\0"
	"__stack_chk_fail\0"
	"single_open\0"
	"seq_printf\0"
	"seq_putc\0"
	"module_layout\0"
;

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "E763F2EB07AC8783FDA0B04");
