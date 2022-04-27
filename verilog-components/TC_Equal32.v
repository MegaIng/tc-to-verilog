module TC_Equal32(in0, in1, out);
    input [31:0] in0;
    input [31:0] in1;
    output out;
    
    assign out = (in0 ^ in1) == 32'b0000_0000_0000_0000_0000_0000_0000_0000;
endmodule

