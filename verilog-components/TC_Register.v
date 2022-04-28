module TC_Register (clk, rst, load, save, in, out);
    parameter size = 1;
    input clk;
    input rst;
    input load;
    input save;
    input [size-1:0] in;
    output tri0 [size-1:0] out;
    reg [size-1:0] outval;
    reg [size-1:0] value;
    
    always @ (posedge clk) begin
        if (load)
            outval <= value;
        else
            outval <= {size{1'bZ}};
    end
    always @ (negedge clk or rst) begin
        if (rst)
            value <= {size{1'b0}};
        else if (save)
            value <= in;
    end
    assign out = outval;
endmodule
