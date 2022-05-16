module TC_ProgramWord (clk, rst, address, out0, out1, out2, out3);
    parameter UUID = 0;
    parameter NAME = "";
    parameter BIT_WIDTH = 16;
    parameter BIT_DEPTH = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [15:0] address;
    output reg [BIT_WIDTH-1:0] out0;
    output reg [BIT_WIDTH-1:0] out1;
    output reg [BIT_WIDTH-1:0] out2;
    output reg [BIT_WIDTH-1:0] out3;

    reg [BIT_WIDTH-1:0] mem [0:BIT_DEPTH];
    
    integer fd;
    integer i;

    initial begin
        hexfile = HEX_FILE;
        i = ($value$plusargs(ARG_SIG, hexfile));
        $display("loading %0s", hexfile);
        fd = $fopen(hexfile, "r");
        if (fd) begin
            i = 0;
            while (i < BIT_DEPTH && !$feof(fd)) begin
                mem[i][7:0] = $fgetc(fd);
                if (BIT_WIDTH > 8 && !$feof(fd)) begin
                    mem[i][15:8] = $fgetc(fd);
                    if (BIT_WIDTH > 16 && !$feof(fd)) begin
                        mem[i][23:16] = $fgetc(fd);
                        if (!$feof(fd)) begin
                            mem[i][31:24] = $fgetc(fd);
                            if (BIT_WIDTH > 32 && !$feof(fd)) begin
                                mem[i][39:32] = $fgetc(fd);
                                if (!$feof(fd)) begin
                                    mem[i][47:40] = $fgetc(fd);
                                    if (!$feof(fd)) begin
                                        mem[i][55:48] = $fgetc(fd);
                                        if (!$feof(fd)) begin
                                            mem[i][63:56] = $fgetc(fd);
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
                i = i + 1;
            end
            $display("read %0d bytes from %0d expected bytes", i, BIT_DEPTH);
        end else begin
            $display("file not found");
        end
        $fclose(fd);
        out0 = {BIT_WIDTH{1'b0}};
        out1 = {BIT_WIDTH{1'b0}};
        out2 = {BIT_WIDTH{1'b0}};
        out3 = {BIT_WIDTH{1'b0}};
    end

    always @ (address or rst) begin
        if (rst) begin
            out0 = {BIT_WIDTH{1'b0}};
            out1 = {BIT_WIDTH{1'b0}};
            out2 = {BIT_WIDTH{1'b0}};
            out3 = {BIT_WIDTH{1'b0}};
        end else begin
            out0 = mem[address];
            out1 = mem[address+1];
            out2 = mem[address+2];
            out3 = mem[address+3];
        end
    end
endmodule

