module TC_Program8_1 (clk, rst, address, out);
    parameter MEM_BYTES = 65536;
    parameter HEX_FILE = "test_jumps.mem";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [15:0] address;
    output reg [7:0] out;

    reg [7:0] mem [0:MEM_BYTES];

    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs("HEXFILE=%s", hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
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
