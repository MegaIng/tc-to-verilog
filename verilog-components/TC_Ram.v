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
    integer i;
    always @ (posedge clk) begin
        if (load)
            outval <= mem[address];
        else
            outval <= 8'bZZZZ_ZZZZ;
    end
    always @ (negedge clk or posedge rst) begin
        if (save && !rst)
            mem[address] <= in;
        else if (rst)
		      for (i=0; i<256; i=i+1) mem[i] <= 8'b0000_0000;
    end
	 
    assign out = outval;
endmodule
