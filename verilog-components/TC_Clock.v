module TC_Clock (en, out);
    input en;
    output tri0 [63:0] out;
    reg [63:0] outval;
    
    initial begin
        $timeformat(-6, 0, "us", 8);
    end
    
    always begin
        if (en)
            outval = $time;
        else
            outval = {64{1'bZ}};
    end
    
    assign out = outval;
endmodule
