module TC_Register (clk, rst, load, save, in, out);
    parameter BIT_WIDTH = 1;
    input clk;
    input rst;
    input load;
    input save;
    input [BIT_WIDTH-1:0] in;
    output [BIT_WIDTH-1:0] out;
    reg [BIT_WIDTH-1:0] outval;
    reg [BIT_WIDTH-1:0] value;
    
    initial begin
        outval <= {BIT_WIDTH{1'b0}};
        value <= {BIT_WIDTH{1'b0}};
    end
    
    always @ (posedge clk) begin
        if (load)
            outval <= value;
        else
            outval <= {BIT_WIDTH{1'bZ}};
    end
    always @ (negedge clk or posedge rst) begin
        if (save && !rst)
            value <= in;
        else if (rst)
		      value <= {BIT_WIDTH{1'b0}};
    end

    assign out = outval;
endmodule
