module TC_ByteLessI(a, b, out);
    input signed [7:0] a;
    input signed [7:0] b;
    output out;
    
    assign out = a < b;
endmodule

