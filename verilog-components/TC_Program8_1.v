module TC_Program8_1 (clk, rst, address, out);
    parameter MEM_BYTES = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [15:0] address;
    output reg [7:0] out;

    reg [7:0] mem [0:MEM_BYTES];

    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end else begin
            $display("no file specified");
        end
    end

    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out <= 8'b0000_0000;
        end else begin
            out <= mem[address];
        end
    end
endmodule
