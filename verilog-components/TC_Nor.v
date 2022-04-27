module TC_Nor(a, b, out);
    input a;
    input b;
    output out;
    
    assign out = ~(a | b);
endmodule

