module TC_Equal8(in0, in1, out);
    input [7:0] in0;
    input [7:0] in1;
    output out;
    
    assign out = (in0 ^ in1) == 8'b0000_0000;
endmodule

