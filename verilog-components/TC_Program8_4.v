module TC_Program8_4 (clk, rst, address, out0, out1, out2, out3);
    parameter MEM_BYTES = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [256*8:0] hex_file;
    input clk;
    input rst;
    input [7:0] address;
    output reg [7:0] out0;
    output reg [7:0] out1;
    output reg [7:0] out2;
    output reg [7:0] out3;

    reg [7:0] mem [0:MEM_BYTES];

    initial begin
        hex_file = HEX_FILE;
        if ($value$plusargs(ARG_SIG, hex_file)) begin
            $display("loading %0s", hex_file);
            $readmemh(hex_file, mem);
        end else begin
            $display("no file specified");
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

