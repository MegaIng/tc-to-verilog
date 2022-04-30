module TC_Register (clk, rst, load, save, in, out);
    parameter BIT_WIDTH = 1;
    input clk;
    input rst;
    input load;
    input save;
    input [BIT_WIDTH-1:0] in;
    output tri0 [BIT_WIDTH-1:0] out;
    reg [BIT_WIDTH-1:0] outval;
    reg [BIT_WIDTH-1:0] value;
    
    always @ (posedge clk) begin
        if (load && !rst)
            outval <= value;
        else
            outval <= {BIT_WIDTH{1'bZ}};
    end
    always @ (negedge clk or rst) begin
        if (save && !rst)
            value <= in;
    end
    always @ (posedge rst) begin
        value <= {BIT_WIDTH{1'b0}};
        outval <= {BIT_WIDTH{1'bZ}};
    end
    assign out = outval;
endmodule
