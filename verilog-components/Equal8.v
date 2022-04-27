module TC_Equal8(a, b, out);
    input [7:0] a;
    input [7:0] b;
    output out;
    
    assign out = (a ^ b) == 8'b0000_0000;
endmodule

