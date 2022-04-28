`timescale 10ns / 1ns

module TC_DelayLine_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg in;
    wire out;
    
    // dut instantiation
    TC_DelayLine dut (.clk(clk), .rst(rst), .in(in), .out(out));

    // generate clock
    initial begin
        clk = 1'b0;
        forever #1 clk = ~clk;
    end

    // generate reset
    initial begin
        rst = 1'b1;
        #10
        rst = 1'b0;
    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, in=%b, out=%b\n",
                    $time, in, out);
        
        // generate all input combinations with 200ns delays
		  in = 1'b0;
		  #25
        in = 1'b1;
        #20
        in = 1'b0;
        #25
        in = 1'b1;
        #20
        in = 1'b0;
    end
endmodule

