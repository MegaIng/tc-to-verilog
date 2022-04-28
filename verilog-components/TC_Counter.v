module TC_Counter (clk, rst, save, in, out);
    parameter size = 8;
    parameter count = {size{1'b1}};
    input clk;
    input rst;
    input save;
    input [size-1:0] in;
    output reg [size-1:0] out;
    
    always @ (posedge clk or posedge rst) begin
        if (rst)
            out <= {size{1'b0}};
        else if (save)
            out <= in;
        else
            out <= out + 1;
    end
endmodule
