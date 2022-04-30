module TC_BitMemory (clk, rst, save, in, out);
    input clk;
    input rst;
    input load;
    input save;
    input [0:0] in;
    output tri0 [0:0] out;
    reg [0:0] outval;
    reg [0:0] value;
    
    always @ (posedge clk) begin
        if (!rst)
            outval <= value;
        else
            outval <= 1'bZ;
    end
    always @ (negedge clk or rst) begin
        if (save && !rst)
            value <= in;
    end
    always @ (posedge rst) begin
        value <= 1'b0;
        outval <= 1'bZ;
    end
    assign out = outval;
endmodule
