module TC_Xor8(in0, in1, out);
    input [7:0] in0;
    input [7:0] in1;
    output [7:0] out;
    
    assign out = in0 ^ in1;
endmodule

