`timescale 10ns / 1ns

module TC_Register_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg load;
    reg save;
    reg in;
    wire out;
    
    // dut instantiation
    TC_Register dut (.clk(clk), .rst(rst), .load(load), .save(save), .in(in), .out(out));

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
        $monitor("time=%3d, save=%b, load=%b, in=%b, out=%b\n",
                    $time, save, load, in, out);
        
        // generate all input combinations with 200ns delays
		  load = 1'b0;
		  save = 1'b0;
        in = 1'b1;
        #20
        save = 1'b1;
        #20
        save = 1'b0;
        #20
        load = 1'b1;
        #20
        load = 1'b0;
    end
endmodule

