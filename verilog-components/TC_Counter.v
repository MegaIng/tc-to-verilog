module TC_Counter (clk, rst, save, in, out);
    parameter BIT_WIDTH = 8;
    parameter count = {BIT_WIDTH{1'b1}};
    input clk;
    input rst;
    input save;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;
    reg [BIT_WIDTH-1:0] value;
    
    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out <= {BIT_WIDTH{1'b0}};
            value <= {BIT_WIDTH{1'b0}};
        end else if (save) begin
            out <= value;
            value <= in;
        end else begin
            out <= value;
            value <= value + count;
        end
    end
endmodule
