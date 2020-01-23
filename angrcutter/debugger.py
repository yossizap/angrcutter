import sys, base64, json, os
sys.path.append('/usr/lib/python3.6/lib-dynload')
sys.path.append('/usr/local/lib/python3.6/dist-packages')
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/lib/python3.6/dist-packages')
from angrdbg import *
import cutter

class cutterDebugger(Debugger):
    def __init__(self):
        self.base_addr = None

    def _get_vmmap(self):
        memory_map = cutter.cmdj("dmj")
        maps = []
        for m in memory_map:
            start = m["addr"]
            end = m["addr_end"]
            mapperm = 0
            if "r" in m["perm"]:
                mapperm |= SEG_PROT_R
            if "w" in m["perm"]:
                mapperm |= SEG_PROT_W
            if "x" in m["perm"]:
                mapperm |= SEG_PROT_X
            maps += [(start, end, mapperm, m["name"])]
        return maps
 
    def _get_sections(self):
        sections = cutter.core().getAllSections()

    def before_stateshot(self):
        self.vmmap = self._get_vmmap()
        self.base_addr = self.image_base()

        for sec in cutter.cmdj("iSj"):
            if sec["name"] == load_project().arch.got_section_name or sec["name"] == ".plt.got":
                self.got = (sec["vaddr"], sec["vaddr"] + sec["vsize"])
            elif sec["name"] == ".plt":
                self.plt = (sec["vaddr"], sec["vaddr"] + sec["vsize"])
            elif sec["name"] == ".idata":
                self.plt = (sec["vaddr"], sec["vaddr"] + sec["vsize"])

    def after_stateshot(self, state):
        pass

    def is_active(self):
        return cutter.core().currentlyDebugging

    def input_file(self):
        path = cutter.core().currentlyOpenFile.rstrip()
        return open(path, "rb")

    def image_base(self):
        if self.base_addr is None:
            self.base_addr = int(cutter.cmd("e bin.baddr").strip('\n'), 16)
        return self.base_addr

    def get_byte(self, addr):
        try:
            return ord(base64.b64decode(cutter.cmd("p6e 1 @ %d" % addr)))
        except BaseException:
            return None

    def get_word(self, addr):
        try:
            return struct.unpack(
                "<H", base64.b64decode(cutter.cmd("p6e 2 @ %d" % addr)))[0]
        except BaseException:
            return None

    def get_dword(self, addr):
        try:
            return struct.unpack(
                "<I", base64.b64decode(cutter.cmd("p6e 4 @ %d" % addr)))[0]
        except BaseException:
            return None

    def get_qword(self, addr):
        try:
            return struct.unpack(
                "<Q", base64.b64decode(cutter.cmd("p6e 8 @ %d" % addr)))[0]
        except BaseException:
            return None

    def get_bytes(self, addr, size):
        try:
            return base64.b64decode(cutter.cmd("p6e %d @ %d" % (size, addr)))
        except BaseException:
            return None

    def put_byte(self, addr, value):
        self.put_bytes(addr, chr(value))

    def put_word(self, addr, value):
        self.put_bytes(addr, struct.pack("<H", value))

    def put_dword(self, addr, value):
        self.put_bytes(addr, struct.pack("<I", value))

    def put_qword(self, addr, value):
        self.put_bytes(addr, struct.pack("<Q", value))

    def put_bytes(self, addr, value):
        cutter.cmd("w6d %s @ %d" % (base64.b64encode(value).decode("utf-8"), addr))

    def get_reg(self, name):
        if name == "efl":
            name = "eflags"
        reg = cutter.cmd("dr " + name)
        # Large regs(over 80bits) are returned as hex
        if "0x" in reg:
            val = int(reg, 16)
        else:
            val = int(reg)
        return val

    def set_reg(self, name, value):
        if name == "efl":
            name = "eflags"
        cutter.cmd("dr %s=%d" % (name, value))

    def step_into(self):
        cutter.cmd("ds")

    def run(self):
        cutter.cmd("dc")

    def wait_ready(self):
        pass

    def refresh_memory(self):
        pass

    def seg_by_name(self, name):
        for start, end, perms, mname in self.vmmap:
            if name == mname:
                return Segment(name, start, end, perms)
        return None

    def seg_by_addr(self, addr):
        for start, end, perms, name in self.vmmap:
            if addr >= start and addr < end:
                return Segment(name, start, end, perms)
        return None

    def get_got(self):
        return self.got

    def get_plt(self):
        return self.plt

    def get_idata(self):
        return self.idata

    def resolve_name(self, name):
        try:
            modules = cutter.cmdj("dmmj")
            for m in modules[1:]:
                addr = m["address"]
                lib = os.path.basename(m["name"]).split(".")[0].split("-")[0]
                o = cutter.cmd("dmi* %s %s" % (lib, name))
                for line in o.split("\n"):
                    line = line.split()
                    if len(line) < 4:
                        continue
                    if line[1] == name or line[3] == "sym."+name:
                        return int(line[3], 16)
        except:
            pass
        return None
