module TC_Program8_1 (clk, rst, address, out);
    parameter MEM_BYTES = 256;
    //parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [7:0] address;
    output reg [7:0] out;

    reg [7:0] mem [0:MEM_BYTES];
	 
    integer fd;
    integer i;

    initial begin
        //hexfile <= HEX_FILE;
        i = ($value$plusargs(ARG_SIG, hexfile));
        $display("loading %0s", hexfile);
        fd = $fopen(hexfile, "r");
        if (fd) begin
            i = 0;
            while (!$feof(fd) && i < MEM_BYTES) begin
                mem[i] = $fgetc(fd);
                i = i + 1;
            end
            $display("read %d bytes", i);
        end else begin
            $display("file not found");
        end
        $fclose(fd);
        out = 8'b0000_0000;
    end

    always @ (address or rst) begin
        if (rst) begin
            out = 8'b0000_0000;
        end else begin
            out = mem[address];
        end
    end
endmodule
