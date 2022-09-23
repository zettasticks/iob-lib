ifeq ($(filter iob_edge_detect, $(HW_MODULES)),)

# Add to modules list
HW_MODULES+=iob_edge_detect

# Sources
SRC+=$(BUILD_VSRC_DIR)/iob_edge_detect.v

# Copy the sources to the build directory 
$(BUILD_VSRC_DIR)/iob_edge_detect.v: $(LIB_DIR)/hardware/iob_edge_detect/iob_edge_detect.v
	cp $< $(BUILD_VSRC_DIR)

endif