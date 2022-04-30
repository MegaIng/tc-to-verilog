module TC_DelayLine (clk, rst, in, out);
    parameter BIT_WIDTH = 1;
    input clk;
    input rst;
    input [BIT_WIDTH-1:0] in;
    output [BIT_WIDTH-1:0] out;

    reg [BIT_WIDTH-1:0] outval;
    reg [BIT_WIDTH-1:0] value;
    
    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            outval <= {BIT_WIDTH{1'b0}};
            value <= {BIT_WIDTH{1'b0}};
        end else begin
            outval <= value;
            value <= in;
        end
    end
    assign out = outval;
endmodule
