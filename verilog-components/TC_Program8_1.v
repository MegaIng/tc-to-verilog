module TC_Program8_1 (clk, rst, address, out);
    parameter size = 65536;
    parameter rom = "test_jumps.mem";
    input clk;
    input rst;
    input [15:0] address;
    output reg [7:0] out;

    reg [7:0] mem [size:0];

    initial $readmemh(rom, mem);

    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out <= 8'b0000_0000;
        end else begin
            out <= mem[address];
        end
    end
endmodule
