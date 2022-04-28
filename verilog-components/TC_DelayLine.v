module TC_DelayLine (clk, rst, in, out);
    parameter size = 1;
    input clk;
    input rst;
    input [size-1:0] in;
    output tri0 [size-1:0] out;

    reg [size-1:0] outval;
    reg [size-1:0] value;
    
    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            outval <= {size{1'b0}};
            value <= {size{1'b0}};
        end else begin
            outval <= value;
            value <= in;
        end
    end
    assign out = outval;
endmodule
