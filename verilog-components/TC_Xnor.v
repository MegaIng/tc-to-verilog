module TC_Xnor(in0, in1, out);
    parameter BIT_WIDTH = 1;
    input [BIT_WIDTH-1:0] in0;
    input [BIT_WIDTH-1:0] in1;
    output [BIT_WIDTH-1:0] out;
    
    assign out = in0 ~^ in1;
endmodule

