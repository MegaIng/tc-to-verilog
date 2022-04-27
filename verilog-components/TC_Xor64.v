module TC_Xor64(in0, in1, out);
    input [63:0] in0;
    input [63:0] in1;
    output [63:0] out;
    
    assign out = in0 ^ in1;
endmodule

