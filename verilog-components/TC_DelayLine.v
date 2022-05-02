module TC_DelayLine (clk, rst, in, out);
    parameter BIT_WIDTH = 1;
    input clk;
    input rst;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;

    reg [BIT_WIDTH-1:0] value;
    
    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out <= {BIT_WIDTH{1'b0}};
            value <= {BIT_WIDTH{1'b0}};
        end else begin
            out <= value;
            value <= in;
        end
    end
endmodule
