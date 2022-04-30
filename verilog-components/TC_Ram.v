module TC_Ram (clk, rst, load, save, address, in, out);
    input clk;
    input rst;
    input load;
    input save;
    input [7:0] address;
    input [7:0] in;
    output [7:0] out;
    reg [7:0] outval;
    reg [7:0] mem [0:255];
    always @ (posedge clk) begin
        if (load)
            outval <= mem[address];
        else
            outval <= 8'bZZZZ_ZZZZ;
    end
    always @ (negedge clk or rst) begin
        if (rst)
            mem[address] <= 8'b0000_0000;
        else if (save)
            mem[address] <= in;
    end
    assign out = outval;
endmodule
