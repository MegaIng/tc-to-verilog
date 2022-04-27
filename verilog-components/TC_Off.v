module TC_Off(value);
    parameter size = 1;
    output value;
    
    assign value = {size{1'b0}};
endmodule

