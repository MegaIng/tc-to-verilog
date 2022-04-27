module TC_ByteLessU(a, b, out);
    input [7:0] a;
    input [7:0] b;
    output out;
    
    assign out = a < b;
endmodule

