module TC_Counter (clk, rst, save, in, out);
    parameter BIT_WIDTH = 8;
    parameter count = 1;
    input clk;
    input rst;
    input save;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;
    
    initial begin
        out = {BIT_WIDTH{1'b0}};
    end
    
    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out <= {BIT_WIDTH{1'b0}};
        end else if (save) begin
            out <= in;
        end else begin
            out <= out + count;
        end
    end
    
    always @ (in) begin
        if (!rst && save) begin
            out <= in;
        end
    end
endmodule
