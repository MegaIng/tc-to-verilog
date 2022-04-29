module TC_Program8_4 (clk, rst, address, out0, out1, out2, out3);
    parameter MEM_BYTES = 65536;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEXFILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [15:0] address;
    output reg [7:0] out0;
    output reg [7:0] out1;
    output reg [7:0] out2;
    output reg [7:0] out3;

    reg [7:0] mem [0:MEM_BYTES];

    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end
    end

    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out0 <= 8'b0000_0000;
            out1 <= 8'b0000_0000;
            out2 <= 8'b0000_0000;
            out3 <= 8'b0000_0000;
        end else begin
            out0 <= mem[address];
            out1 <= mem[address+1];
            out2 <= mem[address+2];
            out3 <= mem[address+3];
        end
    end
endmodule

