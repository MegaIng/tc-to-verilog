module TC_Program8_4 (clk, rst, address, out0, out1, out2, out3);
    parameter size = 65536;
    parameter rom = "test_jumps.mem";
    input clk;
    input rst;
    input [15:0] address;
    output reg [7:0] out0;
    output reg [7:0] out1;
    output reg [7:0] out2;
    output reg [7:0] out3;

    reg [7:0] mem [size:0];

    initial $readmemh(rom, mem);

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
