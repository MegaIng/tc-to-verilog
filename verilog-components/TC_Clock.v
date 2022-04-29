module TC_Clock (en, out);
    parameter START_TIME = 0;
    input en;
    output tri0 [63:0] out;
    reg [63:0] outval;
    reg [63:0] starttime;
    
    initial begin
        $timeformat(-6, 0, "us", 8);
    end
    
    always begin
        if (en)
            outval = $time + START_TIME;
        else
            outval = {64{1'bZ}};
    end
    
    assign out = outval;
endmodule
