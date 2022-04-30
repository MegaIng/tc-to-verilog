module TC_Counter (clk, rst, save, in, out);
    parameter BIT_WIDTH = 8;
    parameter count = 1;
    input clk;
    input rst;
    input save;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;
    
    reg [BIT_WIDTH-1:0] out_reg;
    
    initial begin
        out = {BIT_WIDTH{1'b0}};
        out_reg = {BIT_WIDTH{1'b0}};
    end
    
    always @ (negedge clk) begin
        if (!rst) begin
            if (save) begin
                out <= in;
                out_reg <= in + count;
            end else begin
                out <= out_reg;
                out_reg <= out_reg + count;
            end
        end else begin
            out_reg <= {BIT_WIDTH{1'b0}};
        end
    end
    
    //assign out = out_reg;
endmodule
