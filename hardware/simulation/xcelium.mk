# Coverage test name
COV_TEST?=test

SFLAGS = -errormax 15 -status
EFLAGS = $(SFLAGS) -access +wc
ifeq ($(COV),1)
COV_SFLAGS= -LICQUEUE -covoverwrite -covtest $(COV_TEST)
COV_EFLAGS= -covdut $(NAME) -coverage A -covfile xcelium_cov_commands.ccf
endif
VFLAGS+=$(SFLAGS) -update -linedebug -sv -incdir . -incdir ../src  -incdir src

ifeq ($(VCD),1)
VFLAGS+=-define VCD
endif

SIM_SERVER=$(CADENCE_SERVER)
SIM_USER=$(CADENCE_USER)
SIM_SSH_FLAGS=$(CADENCE_SSH_FLAGS)
SIM_SCP_FLAGS=$(CADENCE_SCP_FLAGS)
SIM_SYNC_FLAGS=$(CADENCE_SYNC_FLAGS)

SIM_PROC=xmsim

comp: $(VHDR) $(VSRC)
	xmvlog $(VFLAGS) $(VSRC); xmelab $(EFLAGS) $(COV_EFLAGS) worklib.$(NAME)_tb:module

exec: xmelab.log
	sync && sleep 1 && xmsim $(SFLAGS) $(COV_SFLAGS) worklib.$(NAME)_tb:module
	grep -v xcelium xmsim.log | grep -v xmsim | grep -v "\$finish" >> test.log
ifeq ($(COV),1)
	ls -d cov_work/scope/* > all_ucd_file
	imc -execcmd "merge -runfile all_ucd_file -overwrite -out merge_all"
	imc -init iob_cov_waiver.tcl -exec xcelium_cov.tcl
endif

clean: gen-clean
	@rm -f xmelab.log  xmsim.log  xmvlog.log
	@rm -f iob_cov_waiver.vRefine

very-clean: clean
	@rm -rf cov_work test.log
	@rm -f coverage_report_summary.rpt coverage_report_detail.rpt


.PHONY: comp exec clean very-clean
