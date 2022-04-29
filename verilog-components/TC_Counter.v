module TC_Counter (clk, rst, save, in, out);
    parameter BIT_WIDTH = 8;
    parameter count = {BIT_WIDTH{1'b1}};
    input clk;
    input rst;
    input save;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;
    
    always @ (posedge clk or posedge rst) begin
        if (rst)
            out <= {BIT_WIDTH{1'b0}};
        else if (save)
            out <= in;
        else
            out <= out + 1;
    end
endmodule
